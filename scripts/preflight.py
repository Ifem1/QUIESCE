#!/usr/bin/env python3
from pathlib import Path
import ast, sys
ROOT=Path(__file__).resolve().parents[1]
C=ROOT/'contracts'/'quiesce.py'
s=C.read_text(encoding='utf-8'); t=ast.parse(s)
checks=[]
def ck(cond,msg):
    if not cond: raise AssertionError(msg)
    checks.append(msg)
ck('run_nondet_unsafe' in s,'custom consensus present')
ck('gl.nondet.exec_prompt' in s,'semantic classifier present')
ck('TARGET_REQUIRED' in s and 'SUBSTITUTE_OK' in s and 'NO_TARGET_DEPENDENCY' in s and 'AMBIGUOUS' in s,'bounded verdict taxonomy')
ck('snapshot_commitment_count' in s,'retirement pins commitment set')
ck('COMPONENT_RETIRING' in s,'commitment intake freezes during retirement')
ck('only beneficiary may approve rebind' in s,'beneficiary controls substitution')
ck('v1 automatic replacement must share owner' in s,'automatic replacement authority bounded')
ck('blocking or unresolved commitments remain' in s,'fail-closed finalization')
ck('definition_hash' in s and 'Keccak256' in s,'definition hashes present')
ck('is_quiescent' in s,'stable consumer view')
ck('class Quiesce(gl.Contract)' in s,'single submitted primitive')
ck('https://studio.genlayer.com/api' in (ROOT/'gltest.config.yaml').read_text(),'stable Studionet configured')
ck('61999' in (ROOT/'.env.example').read_text(),'chain id pinned')
# Ensure nondeterminism lives only in classifier path.
parents={}
class V(ast.NodeVisitor):
    stack=[]
    def generic_visit(self,node): parents[id(node)]=tuple(self.stack); super().generic_visit(node)
    def visit_FunctionDef(self,node): self.stack.append(node.name); self.generic_visit(node); self.stack.pop()
V().visit(t)
for n in ast.walk(t):
    if isinstance(n,ast.Call):
        name=''
        x=n.func; parts=[]
        while isinstance(x,ast.Attribute): parts.append(x.attr); x=x.value
        if isinstance(x,ast.Name): parts.append(x.id); name='.'.join(reversed(parts))
        if name.startswith('gl.nondet.'):
            ck('classify_once' in parents[id(n)],f'nondet confined at line {n.lineno}')
# no frontend directories
ck(not (ROOT/'app').exists() and not (ROOT/'frontend').exists() and not (ROOT/'apps').exists(),'no frontend')
print(f"PREFLIGHT PASS: {len(checks)} checks")
