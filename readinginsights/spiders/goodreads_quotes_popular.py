# -*- coding: utf-8 -*-
import scrapy


class GoodreadsQuoteSpider(scrapy.Spider):
    name = "goodreads.quotes.popular"
    allowed_domains = ["goodreads.com"]
    start_urls = ['https://www.goodreads.com/quotes?page=1']

    def parse(self, response):
        x = response
        for quote in x.xpath('//div[@class="quoteDetails"]'):
            book_quotes_link = quote.xpath('.//a[@class="authorOrTitle"]/@href').extract_first()
            item = {
                'text': [s.strip() for s in quote.xpath('./div[@class="quoteText"]/text()').extract()[:-2] if s.strip()],
                'author': quote.xpath('.//span[@class="authorOrTitle"]/text()').extract_first().strip(),
                'author_link': quote.xpath('.//a[@class="leftAlignedImage"]/@href').extract_first(),
                'book_title': quote.xpath('.//a[@class="authorOrTitle"]/text()').extract_first(),
                'book_quotes_link': book_quotes_link,
                'tags': quote.xpath('.//div[@class="quoteFooter"]/div[contains(@class, "smallText")]//a/text()').extract(),
                'likes': quote.xpath('.//div[@class="quoteFooter"]//a[contains(@class, "smallText")]/text()').extract_first(),
                'book_genres': [],
                'full_shelves_link': '',
            }
            if book_quotes_link is None:
                yield item
            else:
                # book_quotes_link = book_quotes_link.replace('/work/quotes/', '/book/show/')
                yield scrapy.Request(
                    response.urljoin(book_quotes_link),
                    callback=self.parse_quote_page,
                    meta={'item': item})
        
        page = x.xpath('//a[@class="next_page"]/@href').extract_first()
        if page:
            yield scrapy.Request(response.urljoin(page))

    def parse_quote_page(self, response):
        # e.g. https://www.goodreads.com/work/quotes/55587025-the-power-of-moments-why-certain-experiences-have-extraordinary-impact
        quote_book_detail_link = response.xpath('//a[@class="bookTitle"]/@href').extract_first()
        yield scrapy.Request(response.urljoin(quote_book_detail_link), callback=self.parse_book_detail_page, meta={'item': response.meta.get('item')})

    def parse_book_detail_page(self, response):
        # e.g. https://www.goodreads.com/book/show/34466952-the-power-of-moments
        item = response.meta.get('item')
        item.update({
            'book_genres': response.xpath('//a[@class="actionLinkLite bookPageGenreLink"]/text()').extract(),
            'full_shelves_link': response.xpath('//a[@class="actionLink right bookPageGenreLink__seeMoreLink"]/@href').extract_first()
        })
        yield item