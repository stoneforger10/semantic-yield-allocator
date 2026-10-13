import ast
import copy
import hashlib
import itertools
import json
import re
from pathlib import Path
from types import SimpleNamespace
import pytest

TREE = ast.parse(Path('contracts/SemanticYieldAllocator.py').read_text())
NS = {'json': json, 'hashlib': hashlib, 're': re}
exec(compile(ast.Module(body=[n for n in TREE.body if isinstance(n, ast.FunctionDef)
     and n.name not in ('clock', 'no_value')], type_ignores=[]), '<actual-helpers>', 'exec'), NS)
RAW = Path('examples/corpus.json').read_bytes()
CORPUS = json.loads(RAW)
CRITERION = 'The passage requires approval from a second person before a sensitive production change.'
NOW = 1791892800  # 2026-10-13T12:00:00Z


def addr(value):
    return '0x' + value.hex() if isinstance(value, bytes) else str(value)


@pytest.fixture
def contract(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    direct_vm.warp('2026-10-13T12:00:00Z')
    return direct_deploy('contracts/SemanticYieldAllocator.py')


def prepare(c, vm, alice, name='demo', sha=None, budget=5, body=RAW):
    vm.mock_web(r'.*/corpus\.json', {'status': 200, 'body': body})
    c.register(name, CRITERION, 'stoneforger10', 'semantic-yield-allocator', 'a' * 40,
               'examples/corpus.json', sha or hashlib.sha256(body).hexdigest(), budget, NOW + 3600)
    return c.experiment_key(addr(alice), name)


def label(vm, value):
    vm.mock_llm(r'(?s).*SEMANTIC YIELD.*', json.dumps({'label': value}))


def reset(vm, value, body=RAW):
    vm.clear_mocks()
    vm.mock_web(r'.*/corpus\.json', {'status': 200, 'body': body})
    label(vm, value)


def test_semantics_changes_next_allocation(contract, direct_vm, direct_alice):
    key = prepare(contract, direct_vm, direct_alice)
    contract.activate(key)
    assert contract.next_trial(key)['arm'] == 0
    label(direct_vm, 'HIT')
    contract.step(key, 0)
    assert contract.next_trial(key)['arm'] == 1  # cold start cannot be bypassed
    reset(direct_vm, 'MISS')
    contract.step(key, 1)
    assert contract.next_trial(key)['arm'] == 0  # HIT/MISS changes adaptive dispatch
    for trial in (2, 3, 4):
        reset(direct_vm, 'HIT')
        contract.step(key, trial)
    job = contract.get_experiment(key)
    assert job['state'] == 'COMPLETE' and job['trials'] == 5
    assert sum(s['attempts'] for s in job['stats']) == 5
    previous = job['activation']['root']
    for trial in range(5):
        record = contract.get_observation(key, trial)
        root = record.pop('root')
        assert root == NS['digest'](record)
        assert record['binding']['prior_root'] == previous
        assert sum(s['attempts'] for s in record['binding']['stats']) == trial
        assert record['binding']['experiment'] == key
        previous = root
    assert previous == job['last_root']
    with direct_vm.expect_revert('closed or stale'):
        contract.step(key, 5)


def test_opposite_labels_reverse_allocation(contract, direct_vm, direct_alice):
    key = prepare(contract, direct_vm, direct_alice)
    contract.activate(key)
    label(direct_vm, 'MISS')
    contract.step(key, 0)
    reset(direct_vm, 'HIT')
    contract.step(key, 1)
    assert contract.next_trial(key)['arm'] == 1


def test_unknown_not_failure_reward(contract, direct_vm, direct_alice):
    key = prepare(contract, direct_vm, direct_alice)
    contract.activate(key)
    label(direct_vm, 'UNKNOWN')
    contract.step(key, 0)
    assert contract.get_experiment(key)['stats'][0] == {'attempts': 1, 'known': 0, 'hits': 0}
    assert contract.next_trial(key)['arm'] == 1


@pytest.mark.parametrize('bad', ['0' * 64, 'f' * 64])
def test_fake_commitment_halts(contract, direct_vm, direct_alice, bad):
    key = prepare(contract, direct_vm, direct_alice, sha=bad)
    contract.activate(key)
    job = contract.get_experiment(key)
    assert job['state'] == 'HALTED' and not job['stats']
    with direct_vm.expect_revert('closed or stale'):
        contract.step(key, 0)


def test_substituted_body_after_activation(contract, direct_vm, direct_alice):
    key = prepare(contract, direct_vm, direct_alice)
    contract.activate(key)
    reset(direct_vm, 'HIT', RAW.replace(b'approval', b'approval FAKE'))
    contract.step(key, 0)
    job = contract.get_experiment(key)
    assert job['state'] == 'HALTED'
    assert job['stats'][0] == {'attempts': 1, 'known': 0, 'hits': 0}
    assert contract.get_observation(key, 0)['label'] == 'UNKNOWN'


def test_http_unavailable_cannot_learn(contract, direct_vm, direct_alice):
    key = prepare(contract, direct_vm, direct_alice)
    contract.activate(key)
    direct_vm.clear_mocks()
    direct_vm.mock_web(r'.*', {'status': 503, 'body': b'not evidence'})
    label(direct_vm, 'HIT')
    contract.step(key, 0)
    assert contract.get_experiment(key)['state'] == 'HALTED'
    assert contract.get_observation(key, 0)['source']['http'] == 503


def test_replay_preserves_immutable_record(contract, direct_vm, direct_alice):
    key = prepare(contract, direct_vm, direct_alice)
    contract.activate(key)
    label(direct_vm, 'HIT')
    contract.step(key, 0)
    before = contract.get_observation(key, 0)
    with direct_vm.expect_revert('closed or stale'):
        contract.step(key, 0)
    assert contract.get_observation(key, 0) == before


def test_anyone_can_step_but_not_change_spec(contract, direct_vm, direct_alice, direct_bob):
    key = prepare(contract, direct_vm, direct_alice)
    before = contract.get_experiment(key)['spec_root']
    direct_vm.sender = direct_bob
    contract.activate(key)
    label(direct_vm, 'MISS')
    contract.step(key, 0)
    assert contract.get_experiment(key)['spec_root'] == before
    other = contract.experiment_key(addr(direct_bob), 'demo')
    assert other != key
    with direct_vm.expect_revert('unknown experiment'):
        contract.step(other, 0)


def test_expiry_permissionless_and_terminal(contract, direct_vm, direct_alice, direct_bob):
    key = prepare(contract, direct_vm, direct_alice)
    contract.activate(key)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert('expiry unavailable'):
        contract.expire(key)
    direct_vm.warp('2026-10-13T13:00:00Z')
    from genlayer import gl
    gl.message_raw['datetime'] = '2026-10-13T13:00:00Z'
    with direct_vm.expect_revert('closed or stale'):
        contract.step(key, 0)
    contract.expire(key)
    assert contract.get_experiment(key)['state'] == 'EXPIRED'
    with direct_vm.expect_revert('activation unavailable'):
        contract.activate(key)


def test_duplicate_and_early_step(contract, direct_vm, direct_alice):
    key = prepare(contract, direct_vm, direct_alice)
    with direct_vm.expect_revert('closed or stale'):
        contract.step(key, 0)
    with direct_vm.expect_revert('duplicate'):
        prepare(contract, direct_vm, direct_alice)


@pytest.mark.parametrize('value', [{'label': True}, {'label': 'HIT', 'score': 1}, {'label': 'PASS'},
    {'label': None}, [], '{"label":"HIT","label":"MISS"}'])
def test_malformed_llm(value):
    assert NS['parse_label'](value) is None


def test_llm_error_rolls_back(contract, direct_vm, direct_alice):
    key = prepare(contract, direct_vm, direct_alice)
    contract.activate(key)
    direct_vm.mock_llm(r'(?s).*SEMANTIC YIELD.*', '{"label":"HIT","score":99}')
    with direct_vm.expect_revert('malformed label'):
        contract.step(key, 0)
    assert contract.get_experiment(key)['trials'] == 0


@pytest.mark.parametrize('mutate', [
    lambda c: c.update(score=100),
    lambda c: c['arms'].append(c['arms'][0]),
    lambda c: c['arms'][0]['items'][0].update(summary='fake'),
    lambda c: c['arms'][0]['items'][1].update(id=c['arms'][0]['items'][0]['id']),
    lambda c: c['arms'][0]['items'][0].update(text=''),
    lambda c: c['arms'][0].update(id='../private'),
])
def test_bad_corpus_schema(mutate):
    corpus = copy.deepcopy(CORPUS)
    mutate(corpus)
    assert NS['parse_corpus'](json.dumps(corpus)) is None


def test_duplicate_json_keys_rejected():
    assert NS['parse_corpus']('{"arms":[],"arms":[]}') is None


@pytest.mark.parametrize('method', ['activate', 'step'])
def test_actual_validator_independently_observes_and_rejects_disagreement(method):
    klass = next(n for n in TREE.body if isinstance(n, ast.ClassDef))
    entry = next(n for n in klass.body if isinstance(n, ast.FunctionDef) and n.name == method)
    callback = next(n for n in entry.body if isinstance(n, ast.FunctionDef) and n.name == 'validate')
    class Return:
        def __init__(self, data):
            self.calldata = data
    calls = []
    report = {'binding': {'experiment': 'a', 'trial': 0}, 'label': 'HIT', 'source': {'hash': 'real'}}
    def observe():
        calls.append(1)
        return copy.deepcopy(report)
    local = {'gl': SimpleNamespace(vm=SimpleNamespace(Return=Return)), 'observe': observe,
             'equivalent': NS['equivalent']}
    exec(compile(ast.Module(body=[callback], type_ignores=[]), '<actual-validator>', 'exec'), local)
    assert local['validate'](Return(report))
    for field, changed in [('label', 'MISS'), ('source', {'hash': 'fake'}), ('binding', {'experiment': 'b', 'trial': 0})]:
        assert not local['validate'](Return(dict(report, **{field: changed})))
    assert len(calls) == 4
    assert not local['validate'](object())
    assert len(calls) == 4


def test_exhaustive_finite_schedule_invariants():
    inventory = NS['manifest'](CORPUS['arms'])
    for labels in itertools.product(['HIT', 'MISS', 'UNKNOWN'], repeat=6):
        stats = [{'attempts': 0, 'known': 0, 'hits': 0} for _ in inventory]
        seen = set()
        for trial, verdict in enumerate(labels):
            i = NS['choose'](stats, inventory)
            position = (i, stats[i]['attempts'])
            assert i >= 0 and position not in seen
            seen.add(position)
            stats[i]['attempts'] += 1
            stats[i]['known'] += verdict != 'UNKNOWN'
            stats[i]['hits'] += verdict == 'HIT'
            assert sum(s['attempts'] for s in stats) == trial + 1
            assert all(0 <= s['hits'] <= s['known'] <= s['attempts'] <= 3 for s in stats)
        assert NS['choose'](stats, inventory) == -1
