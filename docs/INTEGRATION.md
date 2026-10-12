# Integration

A consumer should pin the exact retirement plan hash and call only the stable view:

```python
if not IQuiesce(quiesce_address).view().is_quiescent(plan_id, expected_definition_hash):
    raise gl.vm.UserError("EXPECTED: retirement is not certified quiescent")
```

`examples/retirement_gate.py` contains a minimal consumer and replay guard.

Do not treat `SUBSTITUTE_OK` as final retirement approval. The main contract deliberately requires a beneficiary-approved rebind before the old commitment stops blocking retirement.
