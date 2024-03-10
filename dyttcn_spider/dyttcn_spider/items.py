# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieItem(scrapy.Item):
    translation_name = scrapy.Field()
    movie_name = scrapy.Field()
    year = scrapy.Field()
    region = scrapy.Field()
    category = scrapy.Field()
    language = scrapy.Field()
    subtitles = scrapy.Field()
    release_date = scrapy.Field()
    imdb_rating = scrapy.Field()
    imdb_link = scrapy.Field()
    douban_rating = scrapy.Field()
    douban_link = scrapy.Field()
    director = scrapy.Field()
    actors = scrapy.Field()
    introduction = scrapy.Field()
    play_link = scrapy.Field()
    duration = scrapy.Field()  # 添加duration字段
    image_url = scrapy.Field()
