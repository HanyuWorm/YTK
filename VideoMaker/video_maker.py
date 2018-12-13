import os
import sys
import json
import subprocess
args = sys.argv


name = 'all'
start = 0
end = 0
step = 10

try:
    name = args[1]
    start = args[2]
    end = args[3]
    step = args[4]
except:
	pass
            
def make_video(path, direct):
    # backup(direc)
    #full.mp3 not background music
    #out.mp3 otherwise
    p = subprocess.run(f'ffmpeg -framerate 1 -loop 1 -i {path}{direct}/{direct}.png -i {path}{direct}/out.mp3 -c:v libx264 -c:a  aac -shortest {path}{direct}/out.mp4')
    print(f'success {direct}')

with open('../config.json', encoding="utf-8") as json_data:
    data = json.load(json_data)
    data = dict(data)
    print(data)
if name == 'all':
    # for book in data.values():
    #     # print(data[book])
    #     subprocess.run( f"scrapy crawl {book['website']} -a sub_url={book['url']} -a start_chap={book['start_chapter']} -a end_chap={book['lastest_chapter']}" )
    print('dang phat trien')
else:
    book = data[name]
    if int(start) == 0:
        start = book['start_chapter']
    if int(end) == 0:
        end = book['lastest_chapter']
    
    step = book['chapter_per_video']
    start = int(start)
    end = int(end)
    path = f'../data/{book["name"]}/'

    

    for i in range(start, end + 1, step):
        start_chapter = i
        if  i + step - 1 < end:
            end_chapter = i + step - 1
        else:
            end_chapter = end
        if os.path.exists(f'{path}chuong-{start_chapter}-{end_chapter}/out.mp4'):
            print(f'chuong-{start_chapter}-{end_chapter} out.mp4 EXIST')
        else:
            make_video(path, f'chuong-{start_chapter}-{end_chapter}')
