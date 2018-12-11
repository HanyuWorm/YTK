from PIL import Image, ImageDraw, ImageFont
import os

def draw_image(chapter):
    image = Image.open('image.png')
    font_type=ImageFont.truetype('arial.ttf', 150)
    draw = ImageDraw.Draw(image)
    draw.text(xy=(220, 100), text=f'chương {chapter}', fill=(194, 213, 43), font=font_type)
#     image.show()
    if f'chuong-{chapter}' not in os.listdir():
            os.mkdir(f'chuong-{chapter}')
    image.save(f"chuong-{chapter}/chuong-{chapter}.png","PNG")
for i in range(501, 1520 + 1):
	draw_image(i)
	print(f'complete {i}')