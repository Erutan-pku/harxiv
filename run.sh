rm -f arxiv_20210529.json
time scrapy crawl arxiv -o arxiv_20210529.json
python3 postdeal.py arxiv_20210529.json arxiv_20210529.html 

