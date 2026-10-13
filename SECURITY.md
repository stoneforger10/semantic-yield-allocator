# Security and trust model

Experimental and unaudited. Do not use for financial decisions, factual truth,
service settlement, clinical decisions or resource access authorization.

- Registration binds authenticated creator, contract address, name, immutable
  criterion, corpus commit/hash, policy, finite budget and deadline.
- Fixed public GitHub raw adapter rejects arbitrary hosts, traversal, mutable refs,
  query strings and private endpoints. No secrets should appear in source artifacts.
- A full-body commitment proves which bytes were inspected, not author honesty or
  independence. Source-relative semantic HIT does not prove external events.
- Corpus authors may cherry-pick/order passages or choose unrepresentative buckets.
  No random sample, IID assumption or unbiased factual population inference exists.
- Schema bounds: 2-4 arms, 2-8 items each, globally unique IDs, 20-1000 characters per
  passage, 32768 response bytes, 2-32 trials, 16 registrations per creator.
- Permissionless stepping cannot replace the selected arm/item, criterion, label
  or corpus. Replay/stale trial numbers fail before HTTP or AI. Terminal jobs cannot reset.
- UNKNOWN is not a negative reward. Unavailable/mismatched evidence halts; budget
  spent before halt remains visible. Permissionless expiry closes unresolved work.
- Deadline limits execution, not historic document age. Transaction time is used,
  not an offchain local clock or caller-provided observed timestamp.
- Every consequential report is independently reconstructed and compared exactly.
  No hash-only semantic verification, leader-only schema acceptance or tolerance.
- Exact agreement is network quorum, not proof that all models are correct. Prompt
  injection and correlated model errors remain risks despite explicit instructions.
- Consensus failures and malformed AI outputs roll back. They may prevent progress
  until expiry. No fake CONFLICTED state is synthesized from a transaction failure.
- All prior observation records stay immutable. Public keys/roots are identifiers,
  not bearer capabilities. No token deposits, approvals, transfers or remote writes.
- No privileged pause, mutable implementation, policy override or emergency drain.

Report reproducible issues privately to the repository owner through GitHub before
publishing exploit details. Never include keys, tokens, keystore passwords or raw
Studio validator configuration in bug reports or proof files.
