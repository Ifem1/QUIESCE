#!/usr/bin/env python3
from pathlib import Path
import hashlib
p=Path(__file__).resolve().parents[1]/'contracts'/'quiesce.py'
data=p.read_bytes()
print('sha256:',hashlib.sha256(data).hexdigest())
print('bytes:',len(data))
