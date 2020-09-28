# -*- coding: utf-8 -*-
import scrapy
from scraper.items import ScraperItem


class LifehackerSpider(scrapy.Spider):
    name = 'lifehacker'
    allowed_domains = ['www.lifehacker.jp']
    start_urls = ['https://www.lifehacker.jp/']     # httpをhttpsに変更

    def parse(self, response):
        for content_item in response.css('div.lh-summary'):
            item = ScraperItem()
            href = content_item.css('h3.lh-summary-title a::attr(href)').extract_first()
            title = content_item.css('h3.lh-summary-title a::text').extract_first()
            item['title'] = title
            url = response.urljoin(href)
            item['url'] = url

            yield scrapy.Request(
                url,
                callback=self.parse_detail,
                meta={'item': item}
            )

    @classmethod
    def parse_detail(cls, response):
        item = response.meta['item']
        str_list = response.css('#realEntryBody *::text').extract()
        item['body'] = ''.join(str_list)
        yield item