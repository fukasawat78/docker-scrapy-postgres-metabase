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

