import subprocess
import warnings
import os
import sys
import matplotlib
matplotlib.use('Agg')

import numpy as np

TRIAL_TIMES = 100
STABILITY_SCRIPT = 'stability_proof.py'
INTERESTED_SCRIPT = 'interested_section.py'

# run interested_section.py only once
print("🔁 Running interested_section.py (once)...")
ret = subprocess.run([sys.executable, INTERESTED_SCRIPT])
if ret.returncode != 0:
    print("❌ interested_section.py failed.")
    sys.exit(1)
print("✅ interested_section.py completed.")

# run stability_proof.py multiple times until no warnings or max trials reached
for trial in range(1, TRIAL_TIMES + 1):
    print(f"\n🔁 Trial {trial}/{TRIAL_TIMES} for stability_proof.py")

    # capture warnings
    result = subprocess.run(
        [sys.executable, STABILITY_SCRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={**os.environ, "MPLBACKEND": "Agg"} 
    )

    stderr_output = result.stderr
    stdout_output = result.stdout

    # check for warnings in stderr
    print(stdout_output)
    if stderr_output:
        print("⚠️  Warnings detected:")
        print(stderr_output)
    else:
        print("✅ No warnings. Training succeeded.")
        break
else:
    print(f"❌ stability_proof.py gave warnings {TRIAL_TIMES} times. Aborting.")
