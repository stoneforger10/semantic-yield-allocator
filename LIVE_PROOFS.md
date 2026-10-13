# Proof matrix

Deployed and exercised on StudioNet. Mocked tests remain separate from onchain proofs.

| Property | Local evidence | Live status |
|---|---|---|
| Source/schema/hash binding | direct activation and substitution tests | Full pinned corpus acquired; fake-body case local only |
| Substantive semantic classification | mocked HIT/MISS/UNKNOWN | HIT and MISS verified; UNKNOWN branch not exercised live |
| Reward changes next allocation | opposite-label dispatch tests | After HIT/MISS, next arm is operations; trial 2 consumed its next passage |
| Trial replay blocked | immutable-record direct test | Expected finalized ERROR after COMPLETE; state unchanged |
| Expiry and terminal states | direct tests | First experiment expired publicly; prior HIT record preserved |
| Independent report verification | extracted actual callbacks, two methods | FINALIZED / SUCCESS / MAJORITY_AGREE; source code independently reconstructs reports |
| Inventory and budget invariant | 729 full schedules | Six unique items inspected, COMPLETE, exact counters and root chain verified |
| Injection fixture | malformed-response and UNKNOWN tests are mocked | Observed MISS, not prompt-preferred UNKNOWN; no universal injection-resistance claim |

Synthetic fixtures demonstrate source-relative selection only, not external
service delivery, actual production policies or verified reality.

## Source and identity

- [Deployed contract](https://explorer-studio.genlayer.com/address/0xD6EE361549A61A0fd9138FFC9dD766cEA36cfF47)
- [Exact published contract source](https://github.com/stoneforger10/semantic-yield-allocator/blob/33d233ebd5d35aaad14e35d0ac096944de79f791/contracts/SemanticYieldAllocator.py)
- Normalized deployed source SHA-256: `caf9da79dcbb3e3f74bc9354871cb00acf9470f822c90c9c41e1c7f2f1bdc353`.
- [Commit-pinned synthetic corpus](https://raw.githubusercontent.com/stoneforger10/semantic-yield-allocator/33d233ebd5d35aaad14e35d0ac096944de79f791/examples/corpus.json)
- Corpus raw SHA-256: `99669ef5272353aeccf714b2e30573fcbea5659e700418121bde6ef7b3d71ab6`; 915 bytes.
- Dedicated public test signer: `0x7a413BB4AB62E31d62d4cD9efC8C8a8Dae37FB42`. Encrypted-keystore signing; no funds moved.
- Complete experiment `demo-v2`: `aa7654adecbdfb720956cb01a329c35bcb157fb68d5c87605d96b96602fe1ad8`.
- Older expired experiment `demo`: `cfde0f0f540e6ca0a1f293a4239b4845f0036e2c140e91b97504c587655c620f`.

## Finalized receipts

Every row except the last was independently checked as FINALIZED, leader SUCCESS,
MAJORITY_AGREE. The last is an intentional finalized execution ERROR with the
expected `closed or stale trial` message; it is not a successful execution.
No claim of unanimous validator agreement is made.

| Operation | Transaction | Verified effect |
|---|---|---|
| Deploy | [f218588a](https://explorer-studio.genlayer.com/tx/0xf218588acd74bedbf02aec1274f402c71c9b4b42f5890e7e811e3570493028e6) | Contract exists; normalized source exactly matches published file |
| Initial register | [2c394ab7](https://explorer-studio.genlayer.com/tx/0x2c394ab76cc08b3309d5aae3a8cc3d9f5c5ac8d40fa7b59f8ba13e76f8281e5d) | REGISTERED |
| Initial activate | [1aedebe2](https://explorer-studio.genlayer.com/tx/0x1aedebe2c24710ee3659d70e18f4b78e51c1e34ef788caa936a1d99d1ce3285f) | ACTIVE; corpus inventory frozen |
| Initial trial | [6b97d0ea](https://explorer-studio.genlayer.com/tx/0x6b97d0eab89996d51a23220fbb0ae827708d21ed8dada0cf29327c879dedba44) | HIT; one observation |
| Public expiry | [d5c97348](https://explorer-studio.genlayer.com/tx/0xd5c97348ac64057d57f753fdc2050a7d9792bcb1d948db5f09b3bd1edf9a9d85) | EXPIRED; original HIT root preserved |
| Fresh register | [c4f689f2](https://explorer-studio.genlayer.com/tx/0xc4f689f260a02bcb6bf077ebb8dc869c82d8710d964dc23f26e283a15754e9ff) | New immutable identity, same artifact; longer deadline |
| Fresh activate | [17b882ea](https://explorer-studio.genlayer.com/tx/0x17b882eac72edd8207ca69d36374d48d066edd431bf63ccf45fd7f72eb2b855b) | ACTIVE; inventory acquired independently |
| Trial 0 | [c4accea1](https://explorer-studio.genlayer.com/tx/0xc4accea1d646b2cbe21e871ea7f8e23bcb492aac2a017457e0010e7f36748f66) | operations/op-one HIT; cold start selects telemetry |
| Trial 1 | [8302e827](https://explorer-studio.genlayer.com/tx/0x8302e8276fe4a4424a9872345ac6a3eccc2bd779976efb7596a949c67ef83b52) | telemetry/tm-one MISS; next allocation switches to operations |
| Trial 2 | [0fc0bd97](https://explorer-studio.genlayer.com/tx/0x0fc0bd972968ae93a42a089fb7770d6ed1e0fc5559d4475e140706aa6334b946) | operations/op-two HIT; next remains operations |
| Trial 3 | [46144ee0](https://explorer-studio.genlayer.com/tx/0x46144ee0ed11eb26aa5f47ef7a66d859bb24cd9cf51b9cfb975d31bad1c79250) | operations/op-three HIT; operations inventory exhausted |
| Trial 4 | [8390494c](https://explorer-studio.genlayer.com/tx/0x8390494c6355cc2dccc9808eb052872bd2b81a7979683e92f16ecba37de749ce) | telemetry/tm-two MISS |
| Trial 5 | [c7a50d1b](https://explorer-studio.genlayer.com/tx/0xc7a50d1bb464ecb0bfe2f799c49c79204552fc04e8ea4fe87df5ebf8ac99a6a5) | telemetry/tm-three MISS; COMPLETE at six trials |
| Intentional replay | [4509dc28](https://explorer-studio.genlayer.com/tx/0x4509dc28ec9c595b66b66b7a72a11e52c50d18d23ba1c1d15191fdec41b6165e) | Expected ERROR; still COMPLETE, six observations, unchanged root |

## Readback and limitations

Final statistics: operations `{attempts:3, known:3, hits:3}`; telemetry
`{attempts:3, known:3, hits:0}`. Observation chain head:
`0846f750eb30267285578baf965d5800bc3a776e191385ab33004887df735a20`.
The inspector verified every before-statistic, scheduler choice, unique item,
text commitment, source hash, observation root, after-statistic and chain link.

The injection passage returned MISS despite the prompt requesting UNKNOWN for
embedded instructions. It did not earn a HIT, but this is a semantic deviation,
not a demonstrated UNKNOWN/quarantine result or proof of general injection safety.
UNKNOWN handling, bad hashes, HTTP failures and malformed responses have local
mocked tests only. Distributed disagreement has not been deliberately induced.

Local validation: GenVM lint and SDK semantics pass (informational newer-runner
warning); 28 tests pass, including 729 complete label schedules; 3 SDK encoding
roundtrips pass. Tests are not a production security audit.

Read-only verification:

```powershell
node scripts/check.mjs --source 0xD6EE361549A61A0fd9138FFC9dD766cEA36cfF47
node scripts/inspect.mjs 0xD6EE361549A61A0fd9138FFC9dD766cEA36cfF47 0x7a413BB4AB62E31d62d4cD9efC8C8a8Dae37FB42 demo-v2 COMPLETE
node scripts/check.mjs --error 0x4509dc28ec9c595b66b66b7a72a11e52c50d18d23ba1c1d15191fdec41b6165e 'closed or stale trial'
```

The original experiment's two-hour deadline elapsed during approval/transport
interruptions. It was expired, not reset. The replacement experiment used a new
identity and six-day deadline. Failed read attempts are not transaction proofs;
no uncertain signed payload was blindly rebroadcast.
