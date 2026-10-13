# Contribution form

Contribution Type: Builder → Intelligent Contracts

Contribution Date: 2026-10-13 (actual work date; do not backdate)

## Title (61/80)

SemanticYieldAllocator — Consensus-Grounded Adaptive Sampling

## Notes / Description (977/1000)

```text
SemanticYieldAllocator is a reusable finite-corpus inspection scheduler. A creator freezes a criterion, public Git commit, corpus hash, budget and deadline. The contract fetches the corpus and locks its inventory. Each trial selects an unused passage using integer exploration and smoothed yield; callers cannot choose the passage or submit its label.

Leader and validators independently refetch the source and classify HIT, MISS or UNKNOWN. Exact report agreement binds the passage, source hash, HTTP result, selected item, prior root and before-state. HIT/MISS update counters and change the next allocation. UNKNOWN spends a trial without becoming a failure reward. Observations are immutable and replay-bound; expiry is public and terminal states cannot reset.

StudioNet proofs demonstrate adaptive allocation, budget completion, expiry and replay rejection. Synthetic public fixtures demonstrate source-relative document selection, not factual truth or service delivery.
```

## Evidence URLs

Paste one URL per evidence field, without Markdown brackets. If slots are limited,
prioritize repository, source, LIVE_PROOFS, contract address, adaptive allocation
transaction, completion and replay. The proof ledger links all 14 verified receipts.

- [github.com/stoneforger10/semantic-yield-allocator](https://github.com/stoneforger10/semantic-yield-allocator)
- [github.com/stoneforger10/semantic-yield-allocator/blob/main/contracts/SemanticYieldAllocator.py](https://github.com/stoneforger10/semantic-yield-allocator/blob/main/contracts/SemanticYieldAllocator.py)
- [github.com/stoneforger10/semantic-yield-allocator/blob/main/README.md](https://github.com/stoneforger10/semantic-yield-allocator/blob/main/README.md)
- [github.com/stoneforger10/semantic-yield-allocator/blob/main/LIVE_PROOFS.md](https://github.com/stoneforger10/semantic-yield-allocator/blob/main/LIVE_PROOFS.md)
- [explorer-studio.genlayer.com/address/0xD6EE361549A61A0fd9138FFC9dD766cEA36cfF47](https://explorer-studio.genlayer.com/address/0xD6EE361549A61A0fd9138FFC9dD766cEA36cfF47)
- [explorer-studio.genlayer.com/tx/0xf218588acd74bedbf02aec1274f402c71c9b4b42f5890e7e811e3570493028e6](https://explorer-studio.genlayer.com/tx/0xf218588acd74bedbf02aec1274f402c71c9b4b42f5890e7e811e3570493028e6)
- [explorer-studio.genlayer.com/tx/0x8302e8276fe4a4424a9872345ac6a3eccc2bd779976efb7596a949c67ef83b52](https://explorer-studio.genlayer.com/tx/0x8302e8276fe4a4424a9872345ac6a3eccc2bd779976efb7596a949c67ef83b52)
- [explorer-studio.genlayer.com/tx/0x0fc0bd972968ae93a42a089fb7770d6ed1e0fc5559d4475e140706aa6334b946](https://explorer-studio.genlayer.com/tx/0x0fc0bd972968ae93a42a089fb7770d6ed1e0fc5559d4475e140706aa6334b946)
- [explorer-studio.genlayer.com/tx/0xc7a50d1bb464ecb0bfe2f799c49c79204552fc04e8ea4fe87df5ebf8ac99a6a5](https://explorer-studio.genlayer.com/tx/0xc7a50d1bb464ecb0bfe2f799c49c79204552fc04e8ea4fe87df5ebf8ac99a6a5)
- [explorer-studio.genlayer.com/tx/0x4509dc28ec9c595b66b66b7a72a11e52c50d18d23ba1c1d15191fdec41b6165e](https://explorer-studio.genlayer.com/tx/0x4509dc28ec9c595b66b66b7a72a11e52c50d18d23ba1c1d15191fdec41b6165e)
- [explorer-studio.genlayer.com/tx/0xd5c97348ac64057d57f753fdc2050a7d9792bcb1d948db5f09b3bd1edf9a9d85](https://explorer-studio.genlayer.com/tx/0xd5c97348ac64057d57f753fdc2050a7d9792bcb1d948db5f09b3bd1edf9a9d85)

## Disclosure

Live labels were HIT/MISS, including MISS for the injection fixture despite the
prompt preferring UNKNOWN. UNKNOWN is locally tested only. This is an experimental,
source-relative document-selection primitive, not verified external service
performance, factual truth, a security audit or a points/acceptance guarantee.
