import os
import sys
import json
import subprocess
args = sys.argv


name = 'all'
start = 0
end = 0
voice = 'male'

try:
    name = args[1]
    voice = args[2]
    start = int(args[3])
    end = int(args[4])
except:
	pass

for i in range(start, end + 1):
    subprocess.run(f"python app.py run_all ../data/{name}/chuong-{i} {voice} -1 0")