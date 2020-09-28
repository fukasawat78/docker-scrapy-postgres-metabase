FROM python:3.7.2

ARG project_dir=/app/
RUN mkdir $project_dir
ADD requirements.txt $project_dir

RUN apt-get update -y
RUN apt-get install vim -y

WORKDIR $project_dir
RUN pip install -r requirements.txt

ADD ./scrape $project_dir/scrape
WORKDIR $project_dir/scrape

# プロジェクト追加
#ADD main.py .

#CMD [ "python", "scrapy startproject scraping ." ]