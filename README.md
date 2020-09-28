# Docker Scrape

## cron実行
```bash
$ crontab -e
```

## crontab
```bash
(分)(時)(日)(月)(曜日) 実行するコマンドのパス
例: 0 7 * * * cd /Users/fukasawat78/Github/python-scrape/; bash -l -c 'python3 /Users/fukasawat78/Github/python-scrape\  web_scraper.py'
```