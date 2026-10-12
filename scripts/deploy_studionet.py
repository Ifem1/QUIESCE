#!/usr/bin/env python3
"""Deploy Quiesce with the repository-local GenLayer CLI.

Requires a locally configured/unlocked GenLayer account. This script never
accepts or stores a private key.
"""
from pathlib import Path
import os, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
CLI=ROOT/'node_modules'/'genlayer'/'dist'/'index.js'
if not CLI.exists():
    raise SystemExit('Local CLI missing. Run npm install first.')
NODE=os.environ.get('NODE', 'node')
version=subprocess.check_output([NODE,str(CLI),'--version'],text=True).strip()
if version != '0.39.1':
    raise SystemExit(f'Expected local GenLayer CLI 0.39.1, got {version}')
cmd=[NODE,str(CLI),'deploy','--contract','contracts/quiesce.py','--rpc','https://studio.genlayer.com/api']
print('Running:', ' '.join(cmd))
raise SystemExit(subprocess.call(cmd,cwd=ROOT))
