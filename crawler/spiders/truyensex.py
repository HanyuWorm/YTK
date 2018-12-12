import scrapy
import os
class TruyenSexSpider(scrapy.Spider):
    name = "truyensex.tv"
    url = "http://truyensex.tv/"
    sub_url = ''
    def __init__(self, sub_url='', start_chap=1, end_chap=1, **kwargs):
        self.sub_url = sub_url  
        self.start_chap = int(start_chap)
        self.end_chap = int(end_chap)
        super().__init__(**kwargs)

    def start_requests(self):
        urls = [
            f'{self.url}/{self.sub_url}/{chapter}/' for chapter in range(self.start_chap, self.end_chap + 1)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
                

    def parse(self, response):
        page = response.url.split("/")[-2]
        if 'data' not in os.listdir():
            os.mkdir('data')
        if self.sub_url not in os.listdir('data'):
            os.mkdir(f'data/{self.sub_url}')

        text_file = f'data/{self.sub_url}/chuong-{page}.txt'
        title_file = f'data/{self.sub_url}/chuong-{page}.title'
        
        title = ' '.join(response.css('body > div.logo2 > div:nth-child(4) > h1 > center > a ::text').extract())
        content = '. '.join(response.css('body > div.logo2 > div:nth-child(5) ::text').extract())
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(content)
        with open(title_file, 'w', encoding='utf-8') as f:
            f.write(title)
        self.log('Saved file %s' % text_file)