import json
import subprocess

for i in range(600, 759 + 1):
    subprocess.run(f"python app.py run_all ../data/bach-bao-tong-quan/chuong-{i} hatieumai -1 0")