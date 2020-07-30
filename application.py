from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

path_csv_file = "D:\\git\\24_09_2019_download_repos\\internets3\\amazon_latest_articles.csv"
url = 'https://aws.amazon.com/new/?whats-new-content-all'
existing = ''

"""
Create a script which go to the web site [https://aws.amazon.com/new/?whats-new-content-all]
and extract and save all article from the section "This Week's Featured Announcements" 
(remove all non-relevant links from the results e.g. css files, js files, links to categories of the site).
 If the script runs again it will download only new articles (if any)
"""


def links_csv(path_csv_file):
    """ Opens csv file if exist and get all urls who already been scraped"""
    with open(path_csv_file, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        links = []
        for row in csv_reader:
            print(row[1])
            links.append(row[1])
    return links


try:
    existing = links_csv(path_csv_file)
except Exception as e:
    print(f'file not exist yet {e}')


def amazon(url, existing):
    """ getting all new new article urls"""
    html = urlopen(url)
    aws = BeautifulSoup(html, 'lxml')
    aws_new_articles = aws.find('div', class_='lb-xb-grid lb-row-max-large lb-xb-equal-height lb-snap lb-tiny-xb-1 lb-small-xb-3')
    base_url = 'https://aws.amazon.com'
    articles_urls_all = []
    for link in aws_new_articles.findAll('a'):
        data2 = f'{base_url}{link.attrs["href"]}'
        # print(data2)
        if data2 not in existing:
            articles_urls_all.append(data2)
    return articles_urls_all


csv_file = open(path_csv_file, 'w', newline='', encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['title', 'url', 'description'])
articles_urls = amazon(url, existing)

for url in articles_urls:
    """ description exist in csv file with a lot of empty rows in beginning !!!"""
    html = urlopen(url)
    aws_article = BeautifulSoup(html, 'lxml')
    aws_article_code = aws_article.find('div', class_='nine columns content-with-nav')
    aws_article_code.h1.text
    row = aws_article_code.get_text()
    csv_writer.writerow([aws_article_code.h1.text, url, row])

csv_file.close()




