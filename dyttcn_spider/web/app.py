from flask import Flask, Response
import pymysql

app = Flask(__name__)

# 连接到远程数据库
conn = pymysql.connect(
    host='47.103.43.252',
    user='root',
    password='Xq111111',
    database='my_database',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/m3u')
def provide_m3u():
    try:
        # 从数据库中检索电影信息
        with conn.cursor() as cursor:
            sql = "SELECT movie_name, play_link, category, region, actors, language FROM movies"
            cursor.execute(sql)
            results = cursor.fetchall()

        # 生成M3U文件内容
        m3u_content = "#EXTM3U\n"
        for movie in results:
            m3u_content += f"#EXTINF:-1 tvg-category=\"{movie['category']}\" tvg-region=\"{movie['region']}\" tvg-actors=\"{movie['actors']}\" tvg-language=\"{movie['language']}\",{movie['movie_name']}\n{movie['play_link']}\n"

        # 返回M3U文件内容
        return Response(m3u_content, mimetype='audio/x-mpegurl')

    except pymysql.Error as e:
        return f"Error retrieving data from database: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
