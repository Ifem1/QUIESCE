# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
from dataclasses import dataclass

@gl.contract_interface
class IQuiesce:
    class View:
        def is_quiescent(self, plan_id: u256, expected_definition_hash: str) -> bool: ...
    class Write:
        pass

@allow_storage
@dataclass
class RetirementExecution:
    caller: Address
    plan_id: u256
    action_hash: str

class RetirementGate(gl.Contract):
    quiesce_address: Address
    executions: TreeMap[str, RetirementExecution]

    def __init__(self, quiesce_address: Address):
        self.quiesce_address = quiesce_address

    @gl.public.write
    def execute(self, plan_id: u256, expected_definition_hash: str, action_hash: str) -> None:
        key = str(action_hash).strip().lower()
        if len(key) != 64 or any(c not in "0123456789abcdef" for c in key):
            raise gl.vm.UserError("EXPECTED: action_hash must be lowercase 32-byte hex")
        if key in self.executions:
            raise gl.vm.UserError("EXPECTED: action already executed")
        if not IQuiesce(self.quiesce_address).view().is_quiescent(plan_id, expected_definition_hash):
            raise gl.vm.UserError("EXPECTED: retirement is not certified quiescent")
        receipt = self.executions.get_or_insert_default(key)
        receipt.caller = gl.message.sender_address
        receipt.plan_id = plan_id
        receipt.action_hash = key

    @gl.public.view
    def was_executed(self, action_hash: str) -> bool:
        return str(action_hash).strip().lower() in self.executions
