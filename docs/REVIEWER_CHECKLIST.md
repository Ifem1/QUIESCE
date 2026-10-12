# Reviewer checklist

1. `contracts/quiesce.py` — state machine and custom validator.
2. `tests/direct/test_quiesce.py` — fail-closed and authority tests.
3. `docs/CONSENSUS.md` — why consensus is load-bearing.
4. `docs/SECURITY.md` — bounded registry claim and non-goals.
5. `examples/retirement_gate.py` — optional consumer.
6. `docs/DEPLOYMENT.md` — finalized stable Studionet deployment and lifecycle evidence, including deployed-source parity.

The former `tests/integration/test_quiesce_studionet.py` was a skipped `assert True` placeholder. It has been removed because the pinned test tooling does not provide a reliable read-only Studionet contract-state client; use the recorded finalized transactions and deployment ledger for live evidence. Direct Mode tests remain deterministic local contract tests, not live-chain tests.

Delete GenLayer thought experiment: without semantic consensus, the system can count registered commitments but cannot safely determine whether natural-language terms require the exact retiring component, allow a stated substitute, or create no ongoing target dependency. A central LLM would become the retirement authority; Quiesce instead requires independent validator agreement and then applies deterministic rights-preserving state transitions.
