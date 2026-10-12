# Quiesce

**A contract-only GenLayer primitive that proves a component has no unresolved semantic dependencies before retirement.**

Quiesce is intentionally **not a frontend project**. It is a reusable Intelligent Contract for systems that prospectively register commitments against components and later need a consensus-backed answer to one narrow question:

> Can this component be retired without stranding a still-valid commitment?

The important boundary is that Quiesce does **not** claim to discover every obligation on the internet. It certifies quiescence only against the commitment registry frozen into a retirement plan.

## Why this needs GenLayer

A conventional contract can count explicit references. It cannot reliably interpret statements such as:

- “the Legacy Reporting Engine itself must continue until year end”;
- “monthly reports may be supplied by any functionally equivalent engine”;
- “the old engine produced the migration report, but no future service depends on it.”

Quiesce uses a custom `gl.vm.run_nondet_unsafe` leader/validator path to classify those frozen terms as exactly one of:

- `TARGET_REQUIRED`
- `SUBSTITUTE_OK`
- `NO_TARGET_DEPENDENCY`
- `AMBIGUOUS`

Validators independently perform the same classification. `AMBIGUOUS` fails closed.

The LLM never marks an obligation satisfied, never releases a beneficiary's right, never retires a component, and never moves a commitment to a replacement on its own.

## Core invariant

```text
A component may retire
IFF
its frozen commitment snapshot contains no unresolved dependency.
```

Opening retirement immediately freezes new commitment intake on the target component. This prevents a plan from certifying an old snapshot while new dependencies are still being added.

An unresolved commitment can clear only through one of these paths:

1. **beneficiary release**;
2. **issuer proposes satisfaction + beneficiary confirms**;
3. consensus determines `NO_TARGET_DEPENDENCY`;
4. consensus determines `SUBSTITUTE_OK`, then the beneficiary explicitly approves a deterministic rebind to the frozen replacement component.

`TARGET_REQUIRED`, `AMBIGUOUS`, unassessed commitments, and substitute-eligible commitments that have not actually been rebound all block finalization.

## State machine

```text
COMPONENT
ACTIVE
  |
  | open_retirement()
  v
RETIRING -------------------- cancel ------------------> ACTIVE
  |
  | every snapshot commitment clears
  v
RETIRED
```

Commitments:

```text
ACTIVE ------------------------ beneficiary release ---> RELEASED
  |
  +-- issuer proposes satisfaction --> PROPOSED -- beneficiary confirms --> SATISFIED
  |
  +-- retirement assessment = SUBSTITUTE_OK
       + beneficiary rebinds --------------------------------------------> REBOUND
```

All terminal commitment states are immutable.

## Why substitution is bounded

Quiesce v1 allows automatic rebind only to a replacement component owned by the same controller as the retiring component. That prevents semantic classification from silently transferring an obligation onto an unrelated party.

Even after consensus returns `SUBSTITUTE_OK`, the beneficiary must approve `rebind_commitment()`. The consensus result creates eligibility; it does not manufacture consent.

## Reviewer-facing architecture

```text
prospectively registered commitments
              |
              v
       open retirement
              |
       freeze commitment set
              |
              v
 semantic dependency assessment
    leader + independent validator
              |
              v
 deterministic clearance rules
              |
   unresolved == 0 only
              |
              v
      CERTIFIED QUIESCENT
              |
              v
 downstream retirement/shutdown gate
```

## Repository boundary

The submitted primitive is exactly:

```text
contracts/quiesce.py
```

There is **no frontend, wallet UI, backend, indexer, dashboard, or application flow**.

`examples/retirement_gate.py` is a tiny optional consumer demonstrating that another Intelligent Contract can require a certified Quiesce plan before recording a retirement action. It is not a second product.

## Network baseline

This repository targets only stable GenLayer **Studionet**:

- Chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- Explorer: `https://explorer-studio.genlayer.com`
- repository-local GenLayer CLI: `0.39.1`

The stable Studionet CLI is intentionally installed in this repository through `package.json`; do not rely on a different global CLI.

## Local checks

```bash
npm install
npm run guard:cli
npm run guard:network
python -m py_compile contracts/quiesce.py examples/retirement_gate.py
python scripts/preflight.py
pip install -r requirements-test.txt
pytest tests/direct -v -s
```

Optional full tooling:

```bash
pip install -r requirements.txt
GENVM_VERSION=v0.2.12 genvm-lint check contracts/quiesce.py --json
```

## Direct-mode scenarios included

The committed suite covers:

- owner-only commitment registration;
- retirement freezes commitment intake;
- identity-specific dependency blocks retirement;
- custom validator rejects forged leader class;
- substitute eligibility alone is insufficient;
- beneficiary-controlled rebind;
- `NO_TARGET_DEPENDENCY` clearance;
- ambiguous result fails closed;
- two-party satisfaction lifecycle;
- beneficiary release;
- cancellation re-opens the component;
- replacement ownership boundary;
- definition-hash pinning.

## Live Studionet status

The contract is deployed on stable Studionet 61999 at `0xC220638D1d2DDDcdda64eeE294920Ac88f7f1b22`. Deployment transaction `0x53de94ed7bf150c6edf243f3a7a12f4669c2d439150a0eed7c32c3372cb34767` is `FINALIZED`. The deployed source exactly matches `contracts/quiesce.py`; both SHA-256 hashes are `63921513aec1f6d7181760540052a7e484302ca5775de41fb81ff1babc89973f`.

Live evidence on the [GenLayer Studio Explorer](https://explorer-studio.genlayer.com) (search each transaction hash):

- **Target blocker:** plan 1 assessment `0x70e958ef5f7295ba7db981ac2482660de8243e145cb696b9e466b566487e563f` finalized as `TARGET_REQUIRED`; finalization attempt `0x1cd95a4aff76f622fa2a8a08f2df9404d38cbaa5c3134bedde54e7bf18de2c8d` finalized with leader `ERROR`, leaving plan `OPEN` and unresolved count 1.
- **Beneficiary rebind:** plan 2 assessment `0x4d6f043d4a3ea8448ed01059f385db600566fda041a9387aec309f079c0ad9a2` finalized as `SUBSTITUTE_OK`; pre-rebind finalization `0x89dce452ef60e648981b92b93db33a4274aed643eb87120eb23d8aeead95e888` finalized with leader `ERROR`; beneficiary rebind `0xe364f3c55e749dc75712e6da2cfde34e5a69d249a76e29e04796f247e1bf46d0` finalized with original commitment `REBOUND` and active child commitment 3 on replacement component 2; owner finalization `0x8b4c866720f1c5eed3b98e95b56e6da8e8bd2a4e7c8658345e52a8c1470ef7b6` finalized with plan `CERTIFIED`, target component 3 `RETIRED`, unresolved count 0. Definition hash `eb93c08e5c41ae7cb7cc8691a9ee01559ed882467b033fdbb4fd9406dd983390`; `is_quiescent` returned `true`.
- **Optional consumer:** `retirement_gate.py` at `0xBbb84d818f9348d9f73696F22086eAd2Fa180E2D`, deployment `0x80575aed07a352f6c6e34fcf86184269dea53b3b6319137f785aa304b63e3879` finalized. Its uncertified-plan call `0xbdcacfb6c1d47de9d15c4cece097266ccf70bb28bdb2bc6ca63e3944163d8f98` finalized with leader `ERROR` and no execution recorded; certified-plan call `0xf11de29366a543a48bfe4c473a6d19627740a46b79f29f4dc782b58c06f4715e` finalized successfully and recorded execution. Consumer source SHA-256: `6e3da96ea4e3b34a9d81721580a5008094069a4838595aa11f83cc696eff7bd2` (exact parity).

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for component/commitment setup transactions, all observed final states, and additional source-parity details.

Local gates and deployment evidence are recorded in `BUILD_STATUS.md` and `docs/DEPLOYMENT.md`. The project is pushed to the sole `Ifem1/quiesce` origin on `main`; [GitHub Actions CI passed](https://github.com/Ifem1/QUIESCE/actions/runs/38307214084), including Direct Mode tests and GenVM lint.

## Threat model / honesty

Quiesce protects the integrity of a **registered dependency set**. It does not discover unregistered contracts, off-chain promises, private agreements, hidden counterparties, or facts outside the registry. A consumer should rely on a Quiesce certificate only when the surrounding system requires dependencies to be registered prospectively.

The semantic classifier also does not decide factual completion. Satisfaction requires explicit on-chain party actions; substitution requires beneficiary consent. This keeps the model inside the narrow question it is good at: whether frozen natural-language terms still semantically depend on the target component.
