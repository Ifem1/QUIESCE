# Build status

## Verified in the opened folder

- `npm install` completed. The repository-local GenLayer CLI reports **0.39.1**.
- `npm run guard:cli` passed.
- `npm run guard:network` passed for stable Studionet chain `61999` and RPC `https://studio.genlayer.com/api`.
- `python -m py_compile contracts/quiesce.py examples/retirement_gate.py` passed.
- `python scripts/preflight.py` passed: **15/15 checks**.
- `pytest tests/direct -v -s` passed: **13/13 tests** against the stable GenVM `v0.2.12` runner. The test setup pins this runner so a cached release candidate cannot be selected implicitly.
- `pip install -r requirements.txt` completed.
- `GENVM_VERSION=v0.2.12 genvm-lint check contracts/quiesce.py --json` passed. The contract has 16 public methods: 10 writes and 6 views.
- `npm audit` reported 6 advisories in the pinned CLI dependency tree (4 moderate, 2 critical). `npm audit` succeeds when the npm advisory endpoint is reachable, but the findings are in the CLI's transitive `vitest`/`tinypool`/`uuid` dependencies; I did not replace or upgrade the mandated CLI version.

The CLI guard and deployment helper invoke the local CLI entrypoint through Node, which works on Windows. The test setup includes a Windows-only cleanup workaround for the Direct Mode package's temporary stdin file and passes `Address` values with the SDK type expected by contract storage.

## Live Studionet evidence

- Quiesce deployed using the configured local GenLayer deployer at `0xC220638D1d2DDDcdda64eeE294920Ac88f7f1b22`; deployment transaction `0x53de94ed7bf150c6edf243f3a7a12f4669c2d439150a0eed7c32c3372cb34767` is `FINALIZED` on stable Studionet 61999.
- Retrieved deployed source is exactly equal to `contracts/quiesce.py`. SHA-256 for both is `63921513aec1f6d7181760540052a7e484302ca5775de41fb81ff1babc89973f`.
- Live blocker proof: target 1, replacement 2; commitment 1 was assessed `TARGET_REQUIRED` in finalized transaction `0x70e958ef5f7295ba7db981ac2482660de8243e145cb696b9e466b566487e563f`. Plan 1 has one unresolved commitment. Finalization attempt `0x1cd95a4aff76f622fa2a8a08f2df9404d38cbaa5c3134bedde54e7bf18de2c8d` is `FINALIZED` with leader execution `ERROR`; plan remains `OPEN`, target remains `RETIRING`.
- Live substitute lifecycle: plan 2 assessment `0x4d6f043d4a3ea8448ed01059f385db600566fda041a9387aec309f079c0ad9a2` is `FINALIZED`, verdict `SUBSTITUTE_OK`; pre-rebind finalization attempt `0x89dce452ef60e648981b92b93db33a4274aed643eb87120eb23d8aeead95e888` is `FINALIZED` with leader `ERROR`; beneficiary rebind `0xe364f3c55e749dc75712e6da2cfde34e5a69d249a76e29e04796f247e1bf46d0` is `FINALIZED` and preserves active child commitment 3 on replacement component 2; owner finalization `0x8b4c866720f1c5eed3b98e95b56e6da8e8bd2a4e7c8658345e52a8c1470ef7b6` is `FINALIZED`. Plan 2 is `CERTIFIED`, target component 3 is `RETIRED`, unresolved count is zero, and `is_quiescent(2, eb93c08e5c41ae7cb7cc8691a9ee01559ed882467b033fdbb4fd9406dd983390)` returned `true`.
- The optional `retirement_gate.py` consumer is deployed at `0xBbb84d818f9348d9f73696F22086eAd2Fa180E2D`; source parity hash is `6e3da96ea4e3b34a9d81721580a5008094069a4838595aa11f83cc696eff7bd2`. Uncertified-plan execution `0xbdcacfb6c1d47de9d15c4cece097266ccf70bb28bdb2bc6ca63e3944163d8f98` finalized with leader `ERROR`, `was_executed=false`; certified-plan execution `0xf11de29366a543a48bfe4c473a6d19627740a46b79f29f4dc782b58c06f4715e` finalized successfully, `was_executed=true`.
- The beneficiary's throwaway key was imported only into the user's local GenLayer keystore and unlocked in the OS keychain for the authorized rebind. It is not in the repository.
- Git is initialized in this existing folder on branch `main`; the only remote is `origin https://github.com/Ifem1/quiesce.git`. The final commit is pushed to `Ifem1/quiesce`.
- GitHub Actions CI passed on `main` in run [`38308172914`](https://github.com/Ifem1/QUIESCE/actions/runs/38308172914). The workflow uses Python 3.12, required by the pinned GenLayer testing suite. The full run passed, including all Direct Mode tests and GenVM lint.

See `docs/DEPLOYMENT.md` for complete observed transaction hashes and state.
