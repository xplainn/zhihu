# -*- coding: utf-8 -*-
import scrapy


class PspgameSpider(scrapy.Spider):
    name = 'pspgame'
    allowed_domains = ['games.tgbus.com/psp/']
    start_urls = ['http://games.tgbus.com/psp//']

    def parse(self, response):
        pass
