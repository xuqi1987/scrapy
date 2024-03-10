## 环境安装

### 创建虚拟环境
```
python3 -m venv myenv

```

### 激活虚拟环境: 
```
source myenv/bin/activate
```

### 退出虚拟环境: 当你完成工作后，可以通过以下命令退出虚拟环境
```
deactivate
```


### 确保你已经安装了Scrapy，如果没有安装，可以使用以下命令进行安装：
```
pip install scrapy
```

### 首先，创建一个新的Scrapy项目。在命令行中执行以下命令：

```
scrapy startproject dyttcn_spider
```
### 然后，进入项目目录并创建一个Spider。在命令行中执行以下命令：

```
cd dyttcn_spider
scrapy genspider dyttcn dyttcn.com
``` 

### JavaScript 重定向页面

```
curl https://www.dyttcn.com/
<html id='anticc_http_redirect'><body><a href='/?__HY=38dcd8fd3657b403728216992e0bd0d3a1710049512_1522911'>continue</a></body></html>%
```

### 解决办法

Scrapy 默认情况下无法执行 JavaScript，因此无法直接处理 JavaScript 渲染的页面。但是，你可以结合 Scrapy 和 Splash 来处理 JavaScript 渲染的页面。

Splash 是一个基于 WebKit 的可编程浏览器，可以通过 HTTP API 与其交互。通过将 Splash 集成到 Scrapy 中，你可以使用 Splash 渲染 JavaScript，并获取页面的完整内容。

以下是如何使用 Scrapy 和 Splash 来获取 https://www.dyttcn.com/ 页面的内容的示例代码：

#### 首先，你需要安装 Splash 和 Scrapy-Splash 扩展：

```
pip install scrapy-splash
```
#### 在 Scrapy 项目的 settings.py 文件中添加以下配置：

```
SPLASH_URL = 'http://localhost:8050'  # Splash 的地址
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'  # 使用 Splash 的去重过滤器
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'  # 使用 Splash 的 HTTP 缓存

```

