from scrapy import Spider,Request
from qiushibaike.items import  QiushibaikeItem


class QiushibaikeSpiderSpider(Spider):
    name = 'qiushibaike_spider'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['http://www.qiushibaike.com/']

    def start_requests(self):
        urls = ['https://www.qiushibaike.com/text/page/1/',]
        for url in urls:
            yield Request(url=url,callback=self.parse)

    def parse(self, response):
        Divs = response.xpath('//*[@id="content"]/div/div[2]')
        divs = Divs.xpath('./div')
        for div in divs:
            item = QiushibaikeItem()
            item['author'] = div.xpath('./div[1]/a[2]/h2/text()').get().replace('\n',"")
            item['content'] =div.xpath('./a[1]/div/span/text()').get().replace('\n',"")
            item['_id'] = div.attrib['id']
            yield  item

        next_page = response.xpath('//*[@id="content"]/div/div[2]/ul/li[2]/a').attrib['href']

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)