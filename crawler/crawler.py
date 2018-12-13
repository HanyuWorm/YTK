import os
import sys
import json
import subprocess
args = sys.argv


name = 'all'
start = 0
end = 0

try:
	name = args[1]
	start = args[2]
	end = args[3]
except:
	pass

with open('config.json', encoding="utf-8") as json_data:
    print(json_data)
    data = json.load(json_data)
    data = dict(data)
    print(data)
if name == 'all':
    for book in data.values():
        # print(data[book])
        subprocess.run( f"scrapy crawl {book['website']} -a sub_url={book['url']} -a start_chap={book['start_chapter']} -a end_chap={book['lastest_chapter']}" )
else:
    book = data[name]
    if start == 0:
        book['start_chapter']
    if end == 0:
        book['lastest_chapter']
	
    subprocess.run(f"scrapy crawl {book['website']} -a sub_url={book['url']} -a start_chap={start} -a end_chap={end}")