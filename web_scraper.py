import requests
import datetime
from bs4 import BeautifulSoup
import csv

news_category = input("欲しいカテゴリのニュースを入力してください:")
csv_list = []

def data_get(category):
   """
   データを取得する
   
   """
   url = 'https://news.yahoo.co.jp/categories/' + category
   response = requests.get(url)
   bs = BeautifulSoup(response.text,'html.parser')
   ul_tag = bs.find_all(class_="topicsList_main")
   return ul_tag
   
   
def data_print(data):
   """
   データを表示させる
   
   """
   news = '-----------------------------------'
   csv_list.append([news])
   for li_tag in data[0]:
       title = li_tag.a.getText()
       url2 = li_tag.a.get("href")
       csv_list.append([title,url2])
       print(title,url2)
       
       
def data_write():
   """
   データをCSVに書き込む
   
   """
   t = datetime.date.today()
   fname = "./outputs/yahoo_timeline" + t.strftime("%Y-%m-%d") + ".csv"
   f = open(fname, "a",newline="",encoding='utf-8_sig')
   writecsv = csv.writer(f, lineterminator='\n')
   writecsv.writerows(csv_list)
   f.close()
       
     
def main():
   """
   各関数を実行する
   
   """
   data_get(news_category)
   data_print(data_get(news_category))
   data_write()

if __name__ == '__main__':
  main()
