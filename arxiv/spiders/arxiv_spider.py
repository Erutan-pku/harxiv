import scrapy
from arxiv.items import ArxivItem
import json, codecs

def clean_text(inputt) :
    inputt = [t.strip() for t in inputt.split() if len(t.strip()) > 0]
    return ' '.join(inputt)

class arxivSpider(scrapy.Spider):
    config = json.load(codecs.open('config.json', 'r', 'utf-8'))['spider']
    print(config)
    name = "arxiv"
    allowed_domains = ["arxiv.org"]
    start_urls = [
        # "https://arxiv.org/list/cs.CL/pastweek?skip=0&show=9999",
        "https://arxiv.org/list/{}/pastweek?skip=0&show={}".format(config['domain'], config['top_n']),
    ]

    def parse(self, response):
        dts = response.xpath('//dt')
        dds = response.xpath('//dd')
        for dt, dd in zip(dts, dds) :
            item = ArxivItem()
            item['idt']    = dt.xpath('span/a/@href').extract()[0].split('/')[-1]
            item['url']    = 'https://arxiv.org/pdf/'+ item['idt'] +'.pdf'
            item['absurl'] = 'https://arxiv.org/abs/'+ item['idt']

            item['title'] = clean_text(dd.xpath('.//div[@class="list-title mathjax"]/text()').extract()[-1])
            item['authors'] = dd.xpath('.//div[@class="list-authors"]/a/text()').extract()
            try :
                item['desc'] = clean_text(dd.xpath('.//div[@class="list-comments mathjax"]/text()').extract()[-1])
            except :
                item['desc'] = ''
            try :
                item['jourref'] = clean_text(dd.xpath('.//div[@class="list-journal-ref"]/text()').extract()[-1])
            except :
                item['jourref'] = ''

            item['subj'] = dd.xpath('.//div[@class="list-subjects"]/span[@class="primary-subject"]/text()').extract()[-1]
            item['subj'] = clean_text(' '.join([item['subj']]+dd.xpath('.//div[@class="list-subjects"]/text()').extract()))
            item['subj'] = [t.strip() for t in item['subj'].split(';')]
            yield item
            # print(item)

# time scrapy crawl arxiv -o items.json
"""
time scrapy crawl arxiv -o arxiv_20210529.json

"""
