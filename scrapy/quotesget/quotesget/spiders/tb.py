# -*- coding: utf-8 -*-
import scrapy


class TbSpider(scrapy.Spider):
    name = 'tb'
    allowed_domains = ['s.taobao.com']
    start_urls = ['http://s.taobao.com/search?q=耳机']

    def parse(self, response):
        print('START')
        print(response.css('.item'))
