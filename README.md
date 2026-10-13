# SemanticYieldAllocator

A finite-corpus, consensus-grounded adaptive sampling primitive for GenLayer.
Experimental, unaudited infrastructure. No token custody, truth certificate,
service-delivery assertion, private agent trace, mutable graph or upgrade proxy.

## Problem and boundary

Document-processing applications have a finite inspection budget. Fixed round-robin
sampling wastes inspections on low-yield buckets; trusting a caller's relevance
score lets that caller control the allocation. This contract allocates the next
inspection from immutable source buckets using observed semantic yield.

A conventional contract can calculate allocation scores, but cannot independently
interpret whether a passage meets a natural-language selection criterion.
GenLayer validators acquire the actual corpus bytes and independently classify the
selected passage. Their consequential label updates the scheduler's sufficient
statistics and changes the next bucket. The caller supplies neither a label nor
an authoritative summary and cannot choose the next arm, item or result.

```text
fixed criterion + Git commit + corpus SHA-256 + trial budget
 -> independently fetch/validate complete corpus -> freeze inventory
 -> integer scheduler selects arm and next unused passage
 -> independent refetch + semantic HIT / MISS / UNKNOWN
 -> exact normalized report consensus
 -> append observation + update counts -> choose next trial
```

## Mechanism, not a domain rename

Storage is a bounded sampling experiment with per-arm attempted/known/hit counts,
immutable inventory and separate observation records. There are no graph edges,
versioned mutation proposals, acceptance certificates or consumption gates.
Unlike a policy adoption engine, no baseline policy is replaced. Unlike a work
queue, no FIFO lane or worker lease determines dispatch. Semantic feedback affects
actual remaining inspection allocation.

## State machine

```text
REGISTERED --activate/acquired--> ACTIVE --step--> ACTIVE
     |                               |             |
     +--bad/unavailable--> HALTED     +--budget/exhausted--> COMPLETE
                                     +--bad/unavailable--> HALTED
REGISTERED or ACTIVE --deadline/any caller--> EXPIRED
```

HALTED, COMPLETE and EXPIRED are terminal. Distributed disagreement or malformed
AI output applies no write. It does not falsely record a consensus conflict.
An agreed UNKNOWN consumes one inspection but never increments known or hit
counts. Missing or changed source bodies halt the experiment rather than inventing
failure rewards. Anyone can activate, step or expire; the specification cannot be
edited after registration. No owner veto or unattended pending lease exists.

## Allocation rule

Inspect each nonempty arm once in manifest order. Thereafter select the available
arm maximizing this exact integer heuristic, ties resolved by manifest order:

```text
score = floor((hits + 1) * 10000 / (known + 2))
      + floor(10000 / (attempts + 1))
```

The first term is Laplace-smoothed semantic yield; the second favors less-inspected
arms. This is an explicit heuristic, not a UCB confidence bound, randomized trial,
unbiased estimate or guarantee of optimal allocation. UNKNOWN reduces remaining
inventory but is not treated as a MISS. The corpus author controls inclusion and
ordering; this limitation cannot be solved by hashing or validator agreement.

## Consensus and evidence

The sole adapter constructs `https://raw.githubusercontent.com/OWNER/REPO/COMMIT/PATH`
with a full 40-character commit, restricted path segments and exact SHA-256 of raw
response bytes. Full UTF-8 bodies are size-bounded, never truncated into evidence.
Duplicate keys, IDs and extra schema fields are rejected. Every step refetches the
whole committed corpus and checks the frozen manifest before evaluating text.

Leader and validators independently execute the acquisition and prompt. Exact
canonical report equality includes the experiment/contract/spec binding, trial,
prior root, before-statistics, selected item, transaction timestamp, HTTP status,
raw response hash and size, full passage, and categorical semantic label. No
confidence or numeric tolerance. Deterministic postchecks bind the passage hash to
the selected inventory item. Hash-linked observation roots bind before/after state.

Freshness means acquisition during this transaction and execution before the fixed
deadline. It does **not** mean the historical document was recently published or
its claims remain true. This protocol certifies no external event. Source control,
prompt injection, model errors and consensus liveness remain explicit risks.

## API

`register`, `activate`, `step`, `expire`, `experiment_key`, `get_experiment`,
`next_trial`, `get_observation`. See [architecture](docs/architecture.md),
[threat model](SECURITY.md) and [proof matrix](LIVE_PROOFS.md).

## Install and test

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/genvm-lint check contracts/SemanticYieldAllocator.py --json
.venv/Scripts/python -m pytest tests -q
npm ci
npm run check:sdk
npm install -g genlayer@0.39.2
```

Runner and dependencies are pinned. Direct tests mock HTTP/AI and run the leader
only. Extracted real validator-callback tests check independent execution and
disagreement rejection, not distributed network consensus. 729 complete label
sequences exercise scheduler bounds, unique consumption and exhaustion.
The Windows test cleanup workaround only defers the runner's open temp-file unlink.

## Deploy and interact

```powershell
genlayer network set studionet
genlayer account use YOUR_ENCRYPTED_TEST_KEYSTORE
genlayer account unlock
genlayer deploy --contract contracts/SemanticYieldAllocator.py
# Commit/push corpus first. Compute Get-FileHash examples/corpus.json -Algorithm SHA256.
$deadline=[DateTimeOffset]::UtcNow.ToUnixTimeSeconds()+7200
genlayer write ADDRESS register --args demo 'The passage requires approval from a second person before a sensitive production change.' stoneforger10 semantic-yield-allocator FULL_COMMIT examples/corpus.json RAW_SHA256 5 $deadline
node scripts/inspect.mjs ADDRESS PUBLIC_CREATOR demo
genlayer write ADDRESS activate --args EXPERIMENT_KEY
genlayer write ADDRESS step --args EXPERIMENT_KEY 0
node scripts/inspect.mjs ADDRESS PUBLIC_CREATOR demo
```

Increment trial only after checking the previous finalized successful receipt and
readback. Do not blindly resend an unknown broadcast. `check.mjs --success HASH`
checks FINALIZED, leader SUCCESS and MAJORITY_AGREE; `--source ADDRESS` compares
normalized deployed source; `--error HASH EXPECTED_TEXT` verifies negative execution.
StudioNet is gasless. Signing stays in an encrypted keystore. Public optional
Windows RPC transports never export keys, change OS DNS or retry uncertain sends.

## Demo honesty

`examples/corpus.json` is an authored **synthetic document corpus**, not independent
proof of an actual organization's policies or delivered service. A HIT means only
that fetched passage meets the document-selection criterion. The live demo should
show HIT in operations, MISS in telemetry, then preferential operations allocation,
with replay rejected. The prompt requests UNKNOWN for injection; actual behavior
must be reported rather than assumed. Do not
claim unexecuted cases, unanimity, steward acceptance, points or global novelty.

## Verified StudioNet demonstration

[Contract](https://explorer-studio.genlayer.com/address/0xD6EE361549A61A0fd9138FFC9dD766cEA36cfF47)
matches published source. Six trials reached COMPLETE with labels
`HIT, MISS, HIT, HIT, MISS, MISS`. Feedback changed allocation; the expected replay
failed without state change. A separate original experiment reached EXPIRED with
its previous HIT observation preserved. Thirteen finalized successful receipts
and one expected finalized execution error are listed in [LIVE_PROOFS.md](LIVE_PROOFS.md).

The injection fixture returned MISS, not prompt-preferred UNKNOWN. No live UNKNOWN
branch or universal injection-resistance claim is made; local tests cover UNKNOWN.
This limitation is disclosed in the proof matrix. [SUBMISSION.md](SUBMISSION.md)
contains bounded, evidence-matched contribution text.
