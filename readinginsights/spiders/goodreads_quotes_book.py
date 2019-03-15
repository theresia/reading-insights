# -*- coding: utf-8 -*-
import scrapy


class GoodreadsQuotesBookSpider(scrapy.Spider):
    name = "goodreads.quotes.book"
    allowed_domains = ["goodreads.com"]
    start_urls = ["https://www.goodreads.com/work/quotes/1966734-the-untethered-soul"]

    def parse(self, response):
        pass
        
