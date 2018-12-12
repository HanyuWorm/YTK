from PIL import Image, ImageDraw, ImageFont
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

def draw_image(start_chapter, end_chapter , path, image_name, font_family, font_size, x, y, color):
    text = f'Chương {start_chapter}-{end_chapter}'
    image = Image.open(path + image_name)
    font_type=ImageFont.truetype(font_family, font_size)
    draw = ImageDraw.Draw(image)
    draw.text(xy=(x, y), text=text, fill=color, font=font_type) #color is tuple
    # image.show()
    if f'chuong-{start_chapter}-{end_chapter}' not in os.listdir(path):
        os.mkdir(f'{path}chuong-{start_chapter}-{end_chapter}')
    image.save(f"{path}chuong-{start_chapter}-{end_chapter}/chuong-{start_chapter}-{end_chapter}.png","PNG")

with open('../config.json') as json_data:
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
    image = book['image']

    image_name = image['name']
    font_family = image['font_family']
    font_size = image['font_size']
    x = image['x']
    y = image['y']
    color = (image['color']['r'], image['color']['g'], image['color']['b'])
	
    for i in range(start, end + 1, step):
        start_chapter = i
        if  i + step - 1 < end:
            end_chapter = i + step - 1
        else:
            end_chapter = end
        
        draw_image(start_chapter, end_chapter, path, image_name, font_family, font_size, x, y, color)
        print(f'complete {i}')





