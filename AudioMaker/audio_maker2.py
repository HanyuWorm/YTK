import json
import subprocess

for i in range(500, 1000 + 1):
    subprocess.run(f"python app.py run_all ../data/mao-son-troc-quy-nhan/chuong-{i} leminh")