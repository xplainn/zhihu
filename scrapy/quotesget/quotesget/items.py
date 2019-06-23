# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #quotes
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()


class PspgameItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #quotes
    name = scrapy.Field()
    type = scrapy.Field()
    maker = scrapy.Field()
    release_time = scrapy.Field()
    version = scrapy.Field()
    stars = scrapy.Field()
    details = scrapy.Field()


class ZHUserItem(scrapy.Item):
    id = scrapy.Field()

    url_token = scrapy.Field()

    name = scrapy.Field()

    use_default_avatar = scrapy.Field()

    avatar_url = scrapy.Field()

    avatar_url_template = scrapy.Field()

    is_org = scrapy.Field()

    type = scrapy.Field()

    url = scrapy.Field()

    user_type = scrapy.Field()

    headline = scrapy.Field()

    gender = scrapy.Field()

    is_advertiser = scrapy.Field()


    vip_info = scrapy.Field()
    # is_vip = scrapy.Field()
    #
    # rename_days = scrapy.Field()

    #
    badge = scrapy.Field()

    allow_message = scrapy.Field()

    is_following = scrapy.Field()

    is_followed = scrapy.Field()

    is_blocking = scrapy.Field()

    answer_count = scrapy.Field()

    articles_count = scrapy.Field()

    employments = scrapy.Field()


class ZHUserArticlesItem(scrapy.Item):
    image_url = scrapy.Field()

    updated = scrapy.Field()

    is_labeled = scrapy.Field()

    excerpt = scrapy.Field()

    admin_closed_comment = scrapy.Field()

    excerpt_title = scrapy.Field()

    id = scrapy.Field()

    voteup_count = scrapy.Field()

    upvoted_followees = scrapy.Field()

    can_comment = scrapy.Field()

    author = scrapy.Field()

    url = scrapy.Field()

    comment_permission = scrapy.Field()

    created = scrapy.Field()

    image_width = scrapy.Field()

    content = scrapy.Field()

    comment_count = scrapy.Field()

    linkbox = scrapy.Field()

    title = scrapy.Field()

    voting = scrapy.Field()

    type = scrapy.Field()

    suggest_edit = scrapy.Field()

    is_normal = scrapy.Field()




