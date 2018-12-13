import os
import sys
import json
import subprocess
import threading
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

def run_all(i):
    subprocess.run(f"python app.py run_all ../data/{name}/chuong-{i} {voice} -1 0")

for i in range(start, end + 1):
    threading.Thread(target=run_all, args=([i])).start()
	# t2 = threading.Thread(target=cal_cube, args=(arr,))
    # subprocess.run(f"python app.py run_all ../data/{name}/chuong-{i} {voice} -1 0")