# -*- coding: utf-8 -*-
import scrapy
from ..items import PspgameItem

class PspgameSpider(scrapy.Spider):
    name = 'pspgame'
    allowed_domains = ['games.tgbus.com']
    start_urls = ['http://games.tgbus.com/psp/']

    def parse(self, response):

        # get gameinfo items
        games = response.css(".ml")

        #
        for game in games:
            Item = PspgameItem()

            # get name
            name = game.css(".ml-t a::text").extract_first()

            #
            gameinfos = game.css(".ml-c2 dl dd::text").extract()

            #get the stars of game
            stars = game.css(".ml-c2 dl dd span::text").extract()

            if stars != None or stars != '':
                stars = len(stars)
            else:
                stars = 0

            if len(gameinfos) == 6:
                Item['name'] = name
                Item['type'] = gameinfos[0]
                Item['maker'] = gameinfos[1]
                Item['release_time'] = gameinfos[2]
                Item['version'] = gameinfos[3]
                Item['stars'] = str(stars)
                Item['details'] = gameinfos[5]
            if len(gameinfos) == 5:
                Item['name'] = name
                Item['type'] = gameinfos[0]
                Item['maker'] = gameinfos[1]
                Item['release_time'] = gameinfos[2]
                Item['version'] = ''
                Item['stars'] = str(stars)
                Item['details'] = gameinfos[4]
            yield Item

        nextPageButton = response.css(".b dl dd a::attr(href)").extract()[-1]

        url = self.start_urls[0].replace('psp/', '')

        nextPageUrl = url + nextPageButton

        print(nextPageUrl)

        yield scrapy.Request(url=nextPageUrl, callback=self.parse)

