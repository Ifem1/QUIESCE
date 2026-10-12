import { execFileSync } from 'node:child_process';
import path from 'node:path';
const local = path.join(process.cwd(), 'node_modules', 'genlayer', 'dist', 'index.js');
let out = '';
try { out = execFileSync(process.execPath, [local, '--version'], {encoding:'utf8'}).trim(); }
catch (e) { console.error('Local GenLayer CLI missing. Run npm install.'); process.exit(1); }
if (out !== '0.39.1') { console.error(`Expected local GenLayer CLI 0.39.1, got: ${out}`); process.exit(1); }
console.log(`CLI guard PASS: ${out}`);
