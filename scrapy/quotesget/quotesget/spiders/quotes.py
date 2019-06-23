# -*- coding: utf-8 -*-
import scrapy
from ..items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):

        quotes = response.css('.quote')

        for quote in quotes:
            #item to save every 'quote' item
            item = QuoteItem()

            #To get info of quote
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()

            #append info into item
            item['text'] = text
            item['author'] = author
            item['tags'] = tags

            #???
            yield item

        #get next page
        nextPage = response.css('.pager .next a::attr(href)').extract_first()

        #generate next page's url
        url = response.urljoin(nextPage)

        #request next page and yield
        yield scrapy.Request(url=url, callback=self.parse)

        ##to save the data, the command is 'scrapy crawl quotes -o quotes.json'
        ##to load json file, use object jsonloader
        ##to save the data to line use command 'scrapy crawl quotes -o quotes.jl'
        ##other format , csv,xml



