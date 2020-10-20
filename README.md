# Docker Scrapy-Postgres-Metabase

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

* [Scrapy Postgres Metabase](#pytorch-template-project)
	* [Usage](#how-to-run)
	* [Organization](#organization)
    * [Acknowledgements](#acknowledgements)

<!-- /code_chunk_output -->

## Usage
Try `docker-compose up -d` to run code.

## Organization

  ```
  docekr-scrapy-postgres-metabase/
    │
    ├── Makefile            <- Makefile with commands like `make data` or `make train`
    ├── README.md           <- The top-level README for developers using this project.
    │
    ├── docker-compose.yml  <- YAML to run docker-compose
    ├── Dockerfile          <- Setup environmemt
    │
    ├── scrape/
    │   ├── scraper
    │   └── select_sample.py
    │ 
    ├── postgres-data/   
    │ 
    ├── outputs/
    │ 
    ├── initdb/
    │   └── create_table.sql
    │ 
    └── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
                              generated with `pip freeze > requirements.txt`
  ```
  
## Acknowledgements

### scrapy

```
items.py
# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
```

```
cd scraper
scrapy genspider lifehacker www.lifehacker.jp
```


```
lifehacker.py
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
```

```
settings.py
DOWNLOAD_DELAY = 3
FEED_EXPORT_ENCODING = 'utf-8'
ITEM_PIPELINES = {
    'scrapy.pipelines.MachimachiPipeline': 300,
}
```

```
pipeline.py
from configparser import ConfigParser
import logging
import psycopg2
import datetime


class MachimachiPipeline(object):

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.register_datetime = datetime.datetime.now()

    def open_spider(self, spider):
        """
        スパイダーが実行されたときに呼ばれる
        :param spider:実行中のスパイダー
        """
        config = ConfigParser()
        config.read('setting.ini')
        host = config.get('default', 'host')
        port = config.get('default', 'port')
        db_name = config.get('default', 'dbname')
        user = config.get('default', 'user')
        password = config.get('default', 'password')

        logging.info('connecting to db.')
        self.connection = psycopg2.connect('host=%s port=%s dbname=%s user=%s password=%s'
                                           % (host, port, db_name, user, password))
        self.connection.autocommit = False
        self.cursor = self.connection.cursor()
        logging.info('connected to db.')

    def close_spider(self, spider):
        """
        スパイダーの処理が終わるときに呼ばれる
        :param spider:処理中のスパイダー
        """
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        logging.info('close connection to db.')

    def process_item(self, item, spider):
        """
        スクレイピングされた項目毎に呼ばれる
        :param item:スクレイピングで取得したデータ
        :param spider:処理中のスパイダー
        :return:dictデータ
        """
        url = item['url']
        self.cursor.execute('SELECT * FROM contents WHERE (url = %s)', (url,))
        record = self.cursor.fetchone()
        if record is not None:
            logging.info('url is already registered. url:%s' % (url,))
            return item
        else:
            values = (
                item['url'],
                spider.allowed_domains[0],
                self.register_datetime,
                item['title'],
                item['body']
            )
            self.cursor.execute('INSERT INTO contents (url, domain_name, register_date , title, contents)'
                                ' VALUES (%s, %s, %s, %s, %s)', values)
            logging.info('contents is registered!!. url:%s' % (url,))
            return item
```

```
all_run.py
import subprocess
import multiprocessing


def get_crawler_list():
    process = subprocess.Popen('scrapy list', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = process.communicate()
    if process.returncode == 0:
        strings = stdout_data.decode('utf-8').split('\n')
        return list(filter(None, strings))
    else:
        raise RuntimeError()


def execute_scraping(crawler_name):
    cmd = 'scrapy crawl %s --loglevel=INFO' % (crawler_name,)
    subprocess.call(cmd.split())


def main():
    jobs = []
    for crawler_name in get_crawler_list():
        job = multiprocessing.Process(target=execute_scraping, args=(crawler_name,))
        jobs.append(job)
        job.start()

    [job.join() for job in jobs]

    print('finish !!!!')


if __name__ == '__main__':
    main()
```
