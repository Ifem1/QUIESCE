# Reviewer checklist

1. `contracts/quiesce.py` — state machine and custom validator.
2. `tests/direct/test_quiesce.py` — fail-closed and authority tests.
3. `docs/CONSENSUS.md` — why consensus is load-bearing.
4. `docs/SECURITY.md` — bounded registry claim and non-goals.
5. `examples/retirement_gate.py` — optional consumer.
6. `docs/DEPLOYMENT.md` — live proof; review only after placeholders are replaced with real finalized evidence.

Delete GenLayer thought experiment: without semantic consensus, the system can count registered commitments but cannot safely determine whether natural-language terms require the exact retiring component, allow a stated substitute, or create no ongoing target dependency. A central LLM would become the retirement authority; Quiesce instead requires independent validator agreement and then applies deterministic rights-preserving state transitions.
