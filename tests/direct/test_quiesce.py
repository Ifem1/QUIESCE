CONTRACT = "contracts/quiesce.py"
CLASSIFIER = r"You are the Quiesce dependency classifier"
TARGET = "Legacy reporting engine"
TARGET_DESC = "Produces monthly regulatory reports for subscribed counterparties."
REPL = "Reporting engine v2"
REPL_DESC = "Produces the same monthly regulatory reports for subscribed counterparties."
STABLE_GENVM_VERSION = "v0.2.12"

def deploy_quiesce(direct_deploy):
    # Pin Direct Mode to the stable runner. The harness otherwise selects the
    # newest cached runner, which may be a release candidate unrelated to the
    # stable Studionet target.
    return direct_deploy(CONTRACT, sdk_version=STABLE_GENVM_VERSION)

def as_address(raw_address):
    from genlayer import Address
    return Address(raw_address)

def setup_pair(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    c = deploy_quiesce(direct_deploy)
    target = c.create_component(TARGET, TARGET_DESC)
    replacement = c.create_component(REPL, REPL_DESC)
    return c, target, replacement

def test_create_component(direct_vm, direct_deploy, direct_alice):
    c, target, _ = setup_pair(direct_vm, direct_deploy, direct_alice)
    item = c.get_component(target)
    assert item["status_name"] == "ACTIVE"
    assert item["definition_hash"]

def test_only_owner_registers_commitment(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, target, _ = setup_pair(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only component owner"):
        c.register_commitment(target, as_address(direct_bob), "Monthly reports", "Target must issue monthly reports.")

def test_retirement_freezes_new_commitments(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, target, replacement = setup_pair(direct_vm, direct_deploy, direct_alice)
    c.register_commitment(target, as_address(direct_bob), "Reports", "Target must issue reports.")
    c.open_retirement(target, replacement)
    with direct_vm.expect_revert("not accepting commitments"):
        c.register_commitment(target, as_address(direct_bob), "Late add", "Must remain available.")

def test_target_required_blocks_finalization(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, target, replacement = setup_pair(direct_vm, direct_deploy, direct_alice)
    cid = c.register_commitment(target, as_address(direct_bob), "Named support", "The Legacy reporting engine itself must provide support through year end; no substitute is permitted.")
    pid = c.open_retirement(target, replacement)
    direct_vm.mock_llm(CLASSIFIER, "TARGET_REQUIRED")
    assert int(c.assess_commitment(pid, cid)) == 1
    assert direct_vm.run_validator() is True
    with direct_vm.expect_revert("unresolved commitments remain"):
        c.finalize_retirement(pid)

def test_validator_rejects_forged_dependency_class(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, target, replacement = setup_pair(direct_vm, direct_deploy, direct_alice)
    cid = c.register_commitment(target, as_address(direct_bob), "Named support", "The specific target must remain available.")
    pid = c.open_retirement(target, replacement)
    direct_vm.mock_llm(CLASSIFIER, "TARGET_REQUIRED")
    c.assess_commitment(pid, cid)
    direct_vm.clear_mocks()
    direct_vm.mock_llm(CLASSIFIER, "TARGET_REQUIRED")
    assert direct_vm.run_validator(leader_result="NO_TARGET_DEPENDENCY") is False

def test_substitution_requires_beneficiary_rebind(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, target, replacement = setup_pair(direct_vm, direct_deploy, direct_alice)
    cid = c.register_commitment(target, as_address(direct_bob), "Monthly reports", "Monthly reports may be provided by any functionally equivalent reporting engine.")
    pid = c.open_retirement(target, replacement)
    direct_vm.mock_llm(CLASSIFIER, "SUBSTITUTE_OK")
    c.assess_commitment(pid, cid)
    with direct_vm.expect_revert("unresolved commitments remain"):
        c.finalize_retirement(pid)
    direct_vm.sender = direct_bob
    new_id = c.rebind_commitment(pid, cid)
    assert c.get_commitment(cid)["status_name"] == "REBOUND"
    assert c.get_commitment(new_id)["component_id"] == replacement
    direct_vm.sender = direct_alice
    c.finalize_retirement(pid)
    assert c.get_component(target)["status_name"] == "RETIRED"

def test_no_dependency_can_clear_without_rebind(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, target, replacement = setup_pair(direct_vm, direct_deploy, direct_alice)
    cid = c.register_commitment(target, as_address(direct_bob), "Historical mention", "The target produced the initial migration report; future reporting is independent of it.")
    pid = c.open_retirement(target, replacement)
    direct_vm.mock_llm(CLASSIFIER, "NO_TARGET_DEPENDENCY")
    c.assess_commitment(pid, cid)
    c.finalize_retirement(pid)
    plan = c.get_plan(pid)
    assert plan["status_name"] == "CERTIFIED"
    assert c.is_quiescent(pid, plan["definition_hash"]) is True

def test_ambiguous_fails_closed(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, target, replacement = setup_pair(direct_vm, direct_deploy, direct_alice)
    cid = c.register_commitment(target, as_address(direct_bob), "Unclear clause", "Support should continue as appropriate.")
    pid = c.open_retirement(target, replacement)
    direct_vm.mock_llm(CLASSIFIER, "AMBIGUOUS")
    c.assess_commitment(pid, cid)
    progress = c.get_plan_progress(pid)
    assert progress["ambiguous"] == 1
    with direct_vm.expect_revert("unresolved commitments remain"):
        c.finalize_retirement(pid)

def test_mutual_satisfaction_is_terminal(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, target, replacement = setup_pair(direct_vm, direct_deploy, direct_alice)
    cid = c.register_commitment(target, as_address(direct_bob), "One-time report", "Deliver the migration report once.")
    c.propose_satisfaction(cid, "a" * 64)
    direct_vm.sender = direct_bob
    c.confirm_satisfaction(cid)
    direct_vm.sender = direct_alice
    pid = c.open_retirement(target, replacement)
    c.finalize_retirement(pid)
    assert c.get_plan_progress(pid)["clear"] == 1

def test_beneficiary_can_release(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, target, replacement = setup_pair(direct_vm, direct_deploy, direct_alice)
    cid = c.register_commitment(target, as_address(direct_bob), "Support", "Target supplies support.")
    direct_vm.sender = direct_bob
    c.release_commitment(cid)
    direct_vm.sender = direct_alice
    pid = c.open_retirement(target, replacement)
    c.finalize_retirement(pid)
    assert c.is_quiescent(pid, c.get_plan(pid)["definition_hash"])

def test_cancel_reopens_component(direct_vm, direct_deploy, direct_alice, direct_bob):
    c, target, replacement = setup_pair(direct_vm, direct_deploy, direct_alice)
    pid = c.open_retirement(target, replacement)
    c.cancel_retirement(pid)
    assert c.get_component(target)["status_name"] == "ACTIVE"
    c.register_commitment(target, as_address(direct_bob), "New", "New active commitment.")

def test_replacement_must_share_owner(direct_vm, direct_deploy, direct_alice, direct_bob):
    direct_vm.sender = direct_alice
    c = deploy_quiesce(direct_deploy)
    target = c.create_component(TARGET, TARGET_DESC)
    direct_vm.sender = direct_bob
    replacement = c.create_component(REPL, REPL_DESC)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("must share owner"):
        c.open_retirement(target, replacement)

def test_plan_hash_is_required_by_consumer_view(direct_vm, direct_deploy, direct_alice):
    c, target, replacement = setup_pair(direct_vm, direct_deploy, direct_alice)
    pid = c.open_retirement(target, replacement)
    c.finalize_retirement(pid)
    good = c.get_plan(pid)["definition_hash"]
    assert c.is_quiescent(pid, good)
    assert c.is_quiescent(pid, "0" * 64) is False
