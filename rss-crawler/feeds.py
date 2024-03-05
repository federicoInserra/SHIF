feeds = [
    {
        '_id':'economist_finance_economics',
        'config':{
            'lang':'en',
            'url':"https://www.economist.com/finance-and-economics/rss.xml",
            'content_html_selectors':['div.article__body p','article  p[data-component="paragraph"]'],
            'attribution':'The Economist',
            'date_format':"%a, %d %b %Y %H:%M:%S %z",
            'custom_fields':['nasdaq_tickers']
        }
    },
    {
        '_id':'economist_business',
        'config':{
            'lang':'en',
            'url':"https://www.economist.com/business/rss.xml",
            'content_html_selectors':['div.article__body p','article  p[data-component="paragraph"]'],
            'attribution':'The Economist',
            'date_format':"%a, %d %b %Y %H:%M:%S %z",
            'custom_fields':['nasdaq_tickers']
        }
    },
    {
        '_id':'marketwatch',
        'config':{
            'lang':'en',
            'url':"https://feeds.content.dowjones.io/public/rss/mw_bulletins",
            'content_html_selectors':['div.article__body p'],
            'attribution':'Marketwatch',
            'date_format':"%a, %d %b %Y %H:%M:%S %Z"
        }
    },
    {
        '_id':'nasdaq_original',
        'config':{
            'lang':'en',
            'url':"https://www.nasdaq.com/feed/nasdaq-original/rss.xml",
            'content_html_selectors':['div.body__content > p','article div.syndicated-article-body div[class*="text-passage"] > p'],
            'attribution':'Nasdaq',
            'date_format':"%a, %d %b %Y %H:%M:%S %z",
            'custom_fields':['nasdaq_tickers']
        }
    },
    {
        '_id':'nasdaq_commodities',
        'config':{
            'lang':'en',
            'url':"https://www.nasdaq.com/feed/rssoutbound?category=Commodities",
            'content_html_selectors':['div.body__content > p','article div.syndicated-article-body div[class*="text-passage"] > p'],
            'attribution':'Nasdaq',
            'date_format':"%a, %d %b %Y %H:%M:%S %z",
            'custom_fields':['nasdaq_tickers']
        }
    },
    {
        '_id':'nasdaq_etfs',
        'config':{
            'lang':'en',
            'url':"https://www.nasdaq.com/feed/rssoutbound?category=ETFs",
            'content_html_selectors':['div.body__content > p','article div.syndicated-article-body div[class*="text-passage"] > p'],
            'attribution':'Nasdaq',
            'date_format':"%a, %d %b %Y %H:%M:%S %z",
            'custom_fields':['nasdaq_tickers']
        }
    },
    {
        '_id':'nasdaq_ipos',
        'config':{
            'lang':'en',
            'url':"https://www.nasdaq.com/feed/rssoutbound?category=IPOs",
            'content_html_selectors':['div.body__content > p','article div.syndicated-article-body div[class*="text-passage"] > p'],
            'attribution':'Nasdaq',
            'date_format':"%a, %d %b %Y %H:%M:%S %z",
            'custom_fields':['nasdaq_tickers']
        }
    },
    {
        '_id':'nasdaq_options',
        'config':{
            'lang':'en',
            'url':"https://www.nasdaq.com/feed/rssoutbound?category=Options",
            'content_html_selectors':['div.body__content > p','article div.syndicated-article-body div[class*="text-passage"] > p'],
            'attribution':'Nasdaq',
            'date_format':"%a, %d %b %Y %H:%M:%S %z",
            'custom_fields':['nasdaq_tickers']
        }
    },
    {
        '_id':'nasdaq_stocks',
        'config':{
            'lang':'en',
            'url':"https://www.nasdaq.com/feed/rssoutbound?category=Stocks",
            'content_html_selectors':['div.body__content > p','article div.syndicated-article-body div[class*="text-passage"] > p'],
            'attribution':'Nasdaq',
            'date_format':"%a, %d %b %Y %H:%M:%S %z",
            'custom_fields':['nasdaq_tickers']
        }
    },
    {
        '_id':'nasdaq_earnings',
        'config':{
            'lang':'en',
            'url':"https://www.nasdaq.com/feed/rssoutbound?category=Earnings",
            'content_html_selectors':['div.body__content > p','article div.syndicated-article-body div[class*="text-passage"] > p'],
            'attribution':'Nasdaq',
            'date_format':"%a, %d %b %Y %H:%M:%S %z",
            'custom_fields':['nasdaq_tickers']
        }
    },
    {
        '_id':'nasdaq_dividends',
        'config':{
            'lang':'en',
            'url':"https://www.nasdaq.com/feed/rssoutbound?category=Dividends",
            'content_html_selectors':['div.body__content > p','article div.syndicated-article-body div[class*="text-passage"] > p'],
            'attribution':'Nasdaq',
            'date_format':"%a, %d %b %Y %H:%M:%S %z",
            'custom_fields':['nasdaq_tickers']
        }
    },
    {
        '_id':'nasdaq_crypto',
        'config':{
            'lang':'en',
            'url':"https://www.nasdaq.com/feed/rssoutbound?category=Cryptocurrencies",
            'content_html_selectors':['div.body__content > p','article div.syndicated-article-body div[class*="text-passage"] > p'],
            'attribution':'Nasdaq',
            'date_format':"%a, %d %b %Y %H:%M:%S %z",
            'custom_fields':['nasdaq_tickers']
        }
    },
    {
        '_id':'nasdaq_markets',
        'config':{
            'lang':'en',
            'url':"https://www.nasdaq.com/feed/rssoutbound?category=Markets",
            'content_html_selectors':['div.body__content > p','article div.syndicated-article-body div[class*="text-passage"] > p'],
            'attribution':'Nasdaq',
            'date_format':"%a, %d %b %Y %H:%M:%S %z",
            'custom_fields':['nasdaq_tickers']
        }
    },
    # {
    #     '_id':'bbc_world',
    #     'config':{
    #         'lang':'en',
    #         'url':"https://feeds.bbci.co.uk/news/world/rss.xml",
    #         'content_html_selectors':['article > div[data-component="text-block"]'],
    #         'attribution':'BBC',
    #         'date_format':"%a, %d %b %Y %H:%M:%S %Z"
    #     }
    # },
    # {
    #     '_id':'bbc_mundo',
    #     'config':{
    #         'lang':'es',
    #         'url':"https://feeds.bbci.co.uk/mundo/rss.xml",
    #         'content_html_selectors':['main > div > p'],
    #         'attribution':'BBC Mundo',
    #         'date_format':"%a, %d %b %Y %H:%M:%S %Z"
    #     }
    # },
    # {
    #     '_id':'france_24_en',
    #     'config':{
    #         'lang':'en',
    #         'url':"https://www.france24.com/en/rss",
    #         'content_html_selectors':["p.t-content__chapo,div.t-content__body > p"],
    #         'attribution':'France24',
    #         'date_format':"%a, %d %b %Y %H:%M:%S %Z"
    #     }
    # },
    # {
    #     '_id':'france_24_fr',
    #     'config':{
    #         'lang':'fr',
    #         'url':"https://www.france24.com/fr/rss",
    #         'content_html_selector':"p.t-content__chapo,div.t-content__body > p",
    #         'attribution':'France24',
    #         'date_format':"%a, %d %b %Y %H:%M:%S %Z"
    #     }
    # },
    # {
    #     '_id':'france_24_es',
    #     'config':{
    #         'lang':'es',
    #         'url':"https://www.france24.com/es/rss",
    #         'content_html_selector':"p.t-content__chapo,div.t-content__body > p",
    #         'attribution':'France24',
    #         'date_format':"%a, %d %b %Y %H:%M:%S %Z"
    #     }
    # }
]