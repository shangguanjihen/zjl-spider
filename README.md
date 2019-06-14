# zjl-spider
# scrapy框架爬取项目
### 1，知乎用户爬取。爬取每个用户基本信息，再通过粉丝，与关注者，不断爬取更多用户,使用最普通的方法爬取
### 2，笔趣阁小说爬取。爬取笔趣阁各类榜单的前20名的小说，使用CrawlSpider方法爬取
### 3，文轩网站图书信息爬取。爬取文轩网站每个大分类如文学小说，儿童，再爬取大分类中的小分类，如现当代小说，传记.再访问每本图书的详细信息。使用分布式爬取，和splash动态网页获取。这个文轩网站爬取前面比较常规，所谓分布式也只是添加了去重类，新的调度器，item pipeline. 主要在于最后的详细页面，爬不出来页面。开始以为是header头，后来发现没用，只好用splash。所以这里使用了scrapy-redis和scrapy-splash两个相关库。但最后发现好像还是有点问题，用splash爬取还是有点问题，暂时这样，下次使用Selenium再爬下。
### 4, 使用Selenium加scrapy-redis分布式爬取比较完美，能爬取js页面。selenium现在是使用chrome的无头版爬取的，爬取页面后应该等个4，5秒，加载js。然后再使用HtmlResponse构造response响应，HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)。其中因为忽视了allowed_domains，导致一直过滤详情页面的请求，浪费了许多时间，不能够。
