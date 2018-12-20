import scrapy
import os
import re
class TruyenTangThuVienSpider(scrapy.Spider):
    name = "truyen.tangthuvien.vn"
    url = "https://truyen.tangthuvien.vn/doc-truyen"
    sub_url = ''
    def __init__(self, sub_url='', start_chap=1, end_chap=1, **kwargs):
        self.sub_url = sub_url  
        self.start_chap = int(start_chap)
        self.end_chap = int(end_chap)
        super().__init__(**kwargs)

    def start_requests(self):
        urls = [
            f'{self.url}/{self.sub_url}/chuong-{chapter}/' for chapter in range(self.start_chap, self.end_chap + 1)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
                

    def parse(self, response):
        page = response.url.split("/")[-2]
        if 'data' not in os.listdir():
            os.mkdir('data')
        if self.sub_url not in os.listdir('data'):
            os.mkdir(f'data/{self.sub_url}')

        text_file = f'data/{self.sub_url}/{page}.txt'
        title_file = f'data/{self.sub_url}/{page}.title'
        
        title = ' '.join(response.css('body > div.container.body-container > div > div.col-xs-12.chapter > h2 ::text').extract())
        content = '. '.join(response.css('body > div.container.body-container > div > div.col-xs-12.chapter > div.chapter-c.max900 > div > div:nth-child(3) ::text').extract())
        content = re.sub('Chuyện hay nên t đề cử.*',  '', content) 
        content = re.sub('( .  . Siêu phẩm đô thi.*',  '', content) 
        

        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(content)
        with open(title_file, 'w', encoding='utf-8') as f:
            f.write(title)
        self.log('Saved file %s' % text_file)
