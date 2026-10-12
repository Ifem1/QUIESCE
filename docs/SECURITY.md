# Security and scope

## Protected invariants

- A target stops accepting new commitments immediately when retirement opens.
- A retirement plan pins the target definition, optional replacement definition, and exact commitment count.
- Terminal commitment state cannot be reopened.
- The issuer cannot unilaterally mark its own obligation satisfied; beneficiary confirmation is required.
- A substitute-eligible commitment remains blocking until the beneficiary explicitly rebinds it.
- Automatic v1 rebinds cannot move an obligation to a component under another owner.
- `TARGET_REQUIRED`, `AMBIGUOUS`, unassessed, and not-yet-rebound commitments block retirement.
- `is_quiescent` is hash-bound to the exact certified plan definition.

## Deliberate non-goals

Quiesce does not discover unregistered obligations. It does not prove real-world service quality, capability equivalence beyond the stored component descriptions, or private agreements. It does not override beneficiary rights. It does not shut down external infrastructure by itself.

Consumers should use Quiesce only where commitment registration is part of the system's prospective operating discipline.
