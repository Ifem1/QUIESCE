# Consensus design

Quiesce uses one custom `gl.vm.run_nondet_unsafe` boundary: dependency classification for an active commitment in an open retirement plan.

The leader and validator receive the same immutable inputs: target label/description, frozen commitment title/terms, and (if configured) replacement label/description. Both invoke the same bounded classifier independently.

Accepted tokens are exactly `TARGET_REQUIRED`, `SUBSTITUTE_OK`, `NO_TARGET_DEPENDENCY`, and `AMBIGUOUS`. Unknown text normalizes to `AMBIGUOUS` on the leader path; a forged leader token is rejected by the validator.

The validator does not check JSON shape. It independently re-runs the semantic judgment and accepts only exact agreement on the bounded settlement token.

Free-form rationale is intentionally not stored because it is not needed for settlement and would create leader-controlled diagnostic text. The consensus-relevant result is only the bounded class.

All money/rights/state transitions remain deterministic. Consensus cannot release a commitment, confirm satisfaction, approve a beneficiary's substitution, or retire the component.
