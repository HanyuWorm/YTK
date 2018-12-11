import json
import subprocess

for i in range(240, 760 + 1):
    subprocess.run(f"python app.py run_all ../data/bach-bao-tong-quan/chuong-{i} hatieumai -1 0")