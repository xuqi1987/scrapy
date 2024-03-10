import scrapy
from scrapy_splash import SplashRequest
from dyttcn_spider.items import MovieItem

class DyttcnSpider(scrapy.Spider):
    name = 'dyttcn'
    start_urls = ['https://www.dyttcn.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})  # 等待0.5秒确保页面加载完全

    def parse(self, response):
        # 使用Scrapy的CSS选择器提取分类信息和对应链接
        categories = response.css('div#menu ul li a::text').extract()
        category_links = response.css('div#menu ul li a::attr(href)').extract()

        # 遍历每个分类链接，并发送请求，排除指定分类
        for category, link in zip(categories, category_links):
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        # 使用Scrapy的CSS选择器提取每个电影条目的链接
        movie_links = response.css('table.tbspan a.ulink::attr(href)').extract()

        # 遍历每个电影链接，并发送请求
        for movie_link in movie_links:
            yield response.follow(movie_link, callback=self.parse_movie)


    def extract_movie_info(self, response, xpath_expr, keyword):
        info = response.xpath(xpath_expr).extract_first()
        if info:
            info = info.split('　')[-1].strip()
            return {keyword: info}
        else:
            return {keyword: None}

            
    def parse_movie(self, response):
        # 创建一个 MovieItem 对象
        movie_item = MovieItem()

        # 提取信息
        movie_info = {}

        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎译　　名")]/text()', 'translation_name'))
        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎片　　名")]/text()', 'movie_name'))
        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎年　　代")]/text()', 'year'))
        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎地　　区")]/text()', 'region'))
        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎类　　别")]/text()', 'category'))
        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎语　　言")]/text()', 'language'))
        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎字　　幕")]/text()', 'subtitles'))
        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎上映日期")]/text()', 'release_date'))
        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎豆瓣评分")]/text()', 'imdb_rating'))
        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎豆瓣链接")]/text()', 'imdb_link'))
        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎片　　长")]/text()', 'duration'))
        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎导　　演")]/text()', 'director'))
        movie_info.update(self.extract_movie_info(response, '//p[contains(text(), "◎主　　演")]/text()', 'actors'))
        
        # 提取<div style="text-align: center;">下的image URL
        image_url = response.xpath('//div[@style="text-align: center;"]/img/@src').extract_first()


        # 提取播放地址
        play_link = response.css('iframe[src^="https://www.dyttcn.com/m3u8/"]::attr(src)').get().strip()
        if play_link:
            play_link = play_link.split('url=')[-1]

        # 如果 year 不是 2024 或 2023，或 play_link 为空，则丢弃该电影条目
        if movie_info.get('year') not in ['2024', '2023'] or not play_link:
            return

        # 将提取的信息存储在 MovieItem 对象中，仅在信息存在时才进行提取
        movie_item['translation_name'] = movie_info.get('translation_name')
        movie_item['movie_name'] = movie_info.get('movie_name')
        movie_item['year'] = movie_info.get('year')
        movie_item['region'] = movie_info.get('region')
        movie_item['category'] = movie_info.get('category')
        movie_item['language'] = movie_info.get('language')
        movie_item['subtitles'] = movie_info.get('subtitles')
        movie_item['release_date'] = movie_info.get('release_date')
        movie_item['imdb_rating'] = movie_info.get('imdb_rating')
        movie_item['imdb_link'] = movie_info.get('imdb_link')
        movie_item['duration'] = movie_info.get('duration')
        movie_item['director'] = movie_info.get('director')
        movie_item['actors'] = movie_info.get('actors')

        movie_item['play_link'] = play_link

        movie_item['image_url'] = image_url

        self.log(movie_item)
        # 返回 Item 对象
        yield movie_item
