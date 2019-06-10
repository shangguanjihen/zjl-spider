# -*- coding: utf-8 -*-

# Scrapy settings for fenbubook project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'fenbubook'

SPIDER_MODULES = ['fenbubook.spiders']
NEWSPIDER_MODULE = 'fenbubook.spiders'
######################


DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"   #去重类，
SCHEDULER = "scrapy_redis.scheduler.Scheduler"               #调度器，从redis中调度
SCHEDULER_PERSIST = True                                     #调度器持久化，断开后可以继续爬取
REDIS_URL = 'redis://:332512@129.204.204.205:6379'     #远程服务器上redis的地址端口
# Crawl responsibly by identifying yourself (and your website) on the user-agent

SPLASH_URL = 'http://129.204.204.205:8051'                #远程服务器上splash的地址端口
#DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'  #去重类
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage' #缓存存储，scrapy-splash必备
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
##############


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  #'Accept-Language': 'en',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'Referer': 'http://list.winxuan.com/1082?sort=7',
    # 'Host': 'item.winxuan.com',
    # 'Connection': 'keep-alive',
    # 'Cache-Control':'max-age=0',
    # 'Upgrade-Insecure-Requests':'1',
    #'Cookie': 'Hm_lvt_cde2ca53bcf3a8674541df9912d3a49b=1559725324; c=886KBB6T; s=WQQ63F2E; sc=0; __utmc=152562790; acw_tc=781bad3615597298718273957e61c4a26b5164d0a1a2d7629211377861359a; www_token=986a8258195f25a48b836bd216a37bb3; __utma=152562790.1775745090.1559725334.1559803118.1559808797.7; __utmz=152562790.1559808797.7.7.utmcsr=winxuan.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __ozlvd1868=1559810132; acw_sc__v2=5cf8ddf3713ff03be0e03521eea6a100a0dd494e; Hm_lpvt_cde2ca53bcf3a8674541df9912d3a49b=1559814709',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   #'fenbubook.middlewares.FenbubookSpiderMiddleware': 543,
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,  #scrapy-splash必备
    'scrapy_redis.pipelines.RedisPipeline': 400,          #存储item到rides中
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   #'fenbubook.middlewares.FenbubookDownloaderMiddleware': 543,
    'scrapy_splash.SplashCookiesMiddleware': 723,    #scrapy-splash必备
    'scrapy_splash.SplashMiddleware': 725,           #scrapy-splash必备
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,  #scrapy-splash必备
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'fenbubook.pipelines.FenbubookPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
