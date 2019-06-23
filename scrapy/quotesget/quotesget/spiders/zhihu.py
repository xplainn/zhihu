# -*- coding: utf-8 -*-
import json

import scrapy
from ..items import ZHUserItem, ZHUserArticlesItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user = 'shen'

    offset = 0
    limit = 20
    # get user's json info
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    # json details
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'


    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    articles_url = 'https://www.zhihu.com/api/v4/members/{user}/articles?include={include}&offset={offset}&limit={limit}&sort_by=created'
    articles_query = 'data[*].comment_count,suggest_edit,is_normal,thumbnail_extra_info,thumbnail,can_comment,comment_permission,admin_closed_comment,content,voteup_count,created,updated,upvoted_followees,voting,review_info,is_labeled,label_info;data[*].author.badge[?(type=best_answerer)].topics'

    def start_requests(self):
        # o-auth token is not required //2019.6.17

        # followers url
        # url = 'https://www.zhihu.com/api/v4/members/shen/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'

        # follows url
        # url = 'https://www.zhihu.com/api/v4/members/shen/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'

        print('USER')
        yield scrapy.Request(url=self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)
        print('FOLLOWS')
        # yield scrapy.Request(url=self.follows_url.format(user=self.start_user, include=self.follows_query, offset=self.offset, limit=self.limit), callback=self.parse_follows)
        print('FOLLOWERS')
        # yield scrapy.Request(url=self.followers_url.format(user=self.start_user, include=self.followers_query, offset=self.offset, limit=self.limit), callback=self.parse_followers)
        print('ARTICLES')
        yield scrapy.Request(url=self.articles_url.format(user=self.start_user, include=self.articles_query, offset=self.offset, limit=self.limit), callback=self.parse_articles)

    def parse_user(self, response):

        result = json.loads(response.text)

        item = ZHUserItem()

        for field in item.fields:
            if field in result.keys():
                item[field] = str(result.get(field))
        yield item

        yield scrapy.Request(url=self.follows_url.format(user=result['url_token'], include=self.follows_query, offset=self.offset, limit=self.limit), callback=self.parse_follows)
        yield scrapy.Request(url=self.followers_url.format(user=result['url_token'], include=self.follows_query, offset=self.offset, limit=self.limit), callback=self.parse_followers)
        yield scrapy.Request(url=self.articles_url.format(user=result['url_token'], include=self.articles_query, offset=self.offset, limit= self.limit), callback=self.parse_articles)

    def parse_follows(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            print('DATA_LEN')
            print(len(results.get('data')))
            print('DATA_LEN')
            for result in results.get('data'):
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') is False:
            print('------------------------------------')
            next_page = str(results.get('paging').get('next')).replace('https://www.zhihu.com/', 'https://www.zhihu.com/api/v4/')

            print(next_page)
            print('------------------------------------')

            yield scrapy.Request(url=next_page, callback=self.parse_follows)

    def parse_followers(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            print('DATA_LEN')
            print(len(results.get('data')))
            print('DATA_LEN')
            for result in results.get('data'):
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token'), include=self.user_query), callback=self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') is False:

            next_page = str(results.get('paging').get('next')).replace('https://www.zhihu.com/', 'https://www.zhihu.com/api/v4/')

            yield scrapy.Request(url=next_page, callback=self.parse_followers)

    def parse_articles(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            print(len(results.get('data')))
            for data in results.get('data'):

                item = ZHUserArticlesItem()

                for field in item.fields:
                    if field in data.keys():
                        item[field] = data[field]

                yield item
        if 'paging' in results.keys() and results.get('paging').get('is_end') is False:
            next_page = str(results.get('paging').get('next')).replace('https://www.zhihu.com/', 'https://www.zhihu.com/api/v4/')
            yield scrapy.Request(url=next_page, callback=self.parse_articles)
