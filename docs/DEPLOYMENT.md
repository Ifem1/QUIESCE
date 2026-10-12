# Studionet deployment record

Observed live evidence only. Every listed transaction was queried until `FINALIZED` on stable Studionet. Transaction hashes can be searched at the [GenLayer Studio Explorer](https://explorer-studio.genlayer.com); the explorer did not return pages through automated fetch, so transaction-specific explorer URLs are not asserted.

## Network and deployed source

- Network: stable Studionet, chain ID `61999`
- RPC: `https://studio.genlayer.com/api`
- Explorer: `https://explorer-studio.genlayer.com`
- Repository-local GenLayer CLI: `0.39.1`
- Quiesce contract: `0xC220638D1d2DDDcdda64eeE294920Ac88f7f1b22`
- Deployment transaction: `0x53de94ed7bf150c6edf243f3a7a12f4669c2d439150a0eed7c32c3372cb34767` — `FINALIZED`, `MAJORITY_AGREE`
- Deployed source equals `contracts/quiesce.py` exactly. Local and fetched deployed source SHA-256: `63921513aec1f6d7181760540052a7e484302ca5775de41fb81ff1babc89973f`.

The issuer/deployer was the user-confirmed local profile `truss-deployer` (`0x39680bd423437c0eaa18493629652821ec672c61`). The beneficiary used a distinct user-supplied throwaway funded test wallet (`0xD6423aE82a975d55C6CeaC222827A727325e0459`). Its private key was imported only into the user's GenLayer account store, outside this repository; no key or keystore is part of the project.

## Target-specific blocker lifecycle

Target component 1 and replacement component 2 were created by the same issuer. Commitment 1 names the target specifically and excludes substitutions.

| Action | Transaction | Final observed result |
|---|---|---|
| Create target component 1 | `0x1a0342c4943a06e7cbec4b3f0290d2872f0befd424238852fb4c77d6b476cc8f` | `FINALIZED`; component `ACTIVE` |
| Create replacement component 2 | `0x24caa6a32ffb40c4ff605adaf14f0d37ac554ec490eb5e054007bb1ea5af4390` | `FINALIZED`; component `ACTIVE` |
| Register target-specific commitment 1 | `0xf118ecf7b007a051678e5b5f9bf9bf5c309be4ac097b00bb6dedd552c2468795` | `FINALIZED`; commitment `ACTIVE` |
| Open plan 1, target 1 / replacement 2 | `0x73ce6208410a8137c3c313eef3dd50d08df9810d7a8ab96ead88772524cd4bc7` | `FINALIZED`; target intake frozen, plan `OPEN` |
| Assess commitment 1 | `0x70e958ef5f7295ba7db981ac2482660de8243e145cb696b9e466b566487e563f` | `FINALIZED`; validator-consensus verdict `TARGET_REQUIRED`; progress `unresolved=1` |
| Attempt to finalize plan 1 | `0x1cd95a4aff76f622fa2a8a08f2df9404d38cbaa5c3134bedde54e7bf18de2c8d` | `FINALIZED`; leader execution `ERROR`; plan remains `OPEN`, target remains `RETIRING`, unresolved count remains 1 |

## Substitute and beneficiary-rebind lifecycle

Target component 3 and replacement component 2 are both owned by the issuer. Commitment 2 explicitly permits any functionally equivalent reporting engine and ongoing continuation on the replacement.

| Action | Transaction | Final observed result |
|---|---|---|
| Create target component 3 | `0xa1ed00eaeb433be8ade9ec25c7ae3bb2f1e42a2daf39c0670e81e97398d7a97a` | `FINALIZED`; component `ACTIVE` |
| Register substitute-eligible commitment 2 | `0xc761b8c83d1b49b50fcffdd80da874fe2a2fd2aa8365abb31c36c099758ea3c6` | `FINALIZED`; commitment `ACTIVE`, beneficiary `0xD6423aE82a975d55C6CeaC222827A727325e0459` |
| Open plan 2, target 3 / replacement 2 | `0x27fe7f76b848b3e88b7b0de87a5a7904af10c33eb685f93ee231e6486458cea2` | `FINALIZED`; plan `OPEN` |
| Assess commitment 2 | `0x4d6f043d4a3ea8448ed01059f385db600566fda041a9387aec309f079c0ad9a2` | `FINALIZED`; validator-consensus verdict `SUBSTITUTE_OK`; `substitute_waiting=1`, `unresolved=1` |
| Attempt to finalize before rebind | `0x89dce452ef60e648981b92b93db33a4274aed643eb87120eb23d8aeead95e888` | `FINALIZED`; leader execution `ERROR`; plan remains `OPEN` |
| Beneficiary rebinds commitment 2 | `0xe364f3c55e749dc75712e6da2cfde34e5a69d249a76e29e04796f247e1bf46d0` | `FINALIZED`, signed by beneficiary `0xD6423aE82a975d55C6CeaC222827A727325e0459`; original 2 becomes `REBOUND`; child commitment 3 is `ACTIVE` on replacement 2 with parent 2; progress `unresolved=0` |
| Owner finalizes plan 2 | `0x8b4c866720f1c5eed3b98e95b56e6da8e8bd2a4e7c8658345e52a8c1470ef7b6` | `FINALIZED`; plan `CERTIFIED`; target 3 `RETIRED` |

Plan 2 definition hash: `eb93c08e5c41ae7cb7cc8691a9ee01559ed882467b033fdbb4fd9406dd983390`. A final read of `is_quiescent(2, "eb93c08e5c41ae7cb7cc8691a9ee01559ed882467b033fdbb4fd9406dd983390")` returned `true`. Final progress was `clear=1`, `unresolved=0`.

## Optional RetirementGate consumer

The example consumer was deployed with the Quiesce address above. Its fetched source exactly matches `examples/retirement_gate.py`; local and deployed SHA-256: `6e3da96ea4e3b34a9d81721580a5008094069a4838595aa11f83cc696eff7bd2`.

- Consumer address: `0xBbb84d818f9348d9f73696F22086eAd2Fa180E2D`
- Deployment transaction: `0x80575aed07a352f6c6e34fcf86184269dea53b3b6319137f785aa304b63e3879` — `FINALIZED`
- Uncertified plan 1 check `is_quiescent(1, "3de0df135fa61f75dd3718590a5b696e9940aa663105d216777bcdb2bbd8938e")` returned `false`.
- Consumer `execute` attempt for plan 1: `0xbdcacfb6c1d47de9d15c4cece097266ccf70bb28bdb2bc6ca63e3944163d8f98` — `FINALIZED`, leader execution `ERROR`; subsequent `was_executed(aaaaaaaa…aaaaaaaa)` returned `false`.
- Consumer `execute` for certified plan 2 and its exact definition hash: `0xf11de29366a543a48bfe4c473a6d19627740a46b79f29f4dc782b58c06f4715e` — `FINALIZED`, leader execution `SUCCESS`; subsequent `was_executed(bbbbbbbb…bbbbbbbb)` returned `true`.
