# 使用官方的 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装 Git
RUN apt-get update && apt-get install -y git

# 克隆 Scrapy 仓库
RUN git clone https://github.com/xuqi1987/scrapy.git

# 进入 Scrapy 项目目录
WORKDIR /app/scrapy/dyttcn_spider/

# 安装依赖
RUN pip install -r requirements.txt

# 添加定时任务脚本
COPY scrapy_crawl.sh /app/scrapy_crawl.sh

# 赋予脚本可执行权限
RUN chmod +x /app/scrapy_crawl.sh

# 设置定时任务
CMD ["sh", "-c", "while true; do /app/scrapy_crawl.sh; sleep 24h; done"]

