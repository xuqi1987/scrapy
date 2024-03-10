import pymysql


import json
class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('movies.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # 将 Item 转换为字典并格式化为 JSON 字符串
        item_dict = dict(item)
        json_str = json.dumps(item_dict, ensure_ascii=False, indent=4)

        # 写入 JSON 字符串到文件中
        self.file.write(json_str)
        self.file.write('\n')  # 添加换行符以保证每个 Item 占用单独一行
        return item


class DyttcnSpiderPipeline:
    def open_spider(self, spider):
        # 连接到 MySQL 数据库
        self.conn = pymysql.connect(
            host='your_host',
            user='your_username',
            password='your_password',
            database='your_database',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        # 关闭数据库连接
        self.conn.close()

    def process_item(self, item, spider):
        # 检查数据库中是否已存在相同电影名的记录
        sql_check = "SELECT * FROM movies WHERE movie_name = %s"
        self.cur.execute(sql_check, (item['movie_name'],))
        result = self.cur.fetchone()

        # 如果电影名已存在，则不执行插入操作
        if result:
            spider.logger.info(f"电影 '{item['movie_name']}' 已存在，跳过插入操作。")
            return item

        # 否则，将提取的数据存储到数据库中
        sql_insert = """
        INSERT INTO movies (translation_name, movie_name, year, region, category, language, subtitles,
                            release_date, imdb_rating, imdb_link, duration, director, actors, play_link, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            item.get('translation_name'),
            item.get('movie_name'),
            item.get('year'),
            item.get('region'),
            item.get('category'),
            item.get('language'),
            item.get('subtitles'),
            item.get('release_date'),
            item.get('imdb_rating'),
            item.get('imdb_link'),
            item.get('duration'),
            item.get('director'),
            item.get('actors'),
            item.get('play_link'),
            item.get('image_url')
        )
        self.cur.execute(sql_insert, values)
        self.conn.commit()

        return item
