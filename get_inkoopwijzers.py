# -*- coding: utf-8 -*-
# encoding=utf8
import csv
import urllib2
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')

data = []
inkoopwijzers_str = "https://www.inkoopwijzers.nl/producten"
limit = 5000
ajax_post_url = "https://www.inkoopwijzers.nl/ajax/get_producten_na_bladeren_new.php"


# calls any url and return as bs4 element
def url_parser(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(clean_url(url), headers=hdr)
    content = urllib2.urlopen(req)
    return parse_content(content)


def fetch_titles(url):
    html_content = url_parser(url)
    return html_content.find('div', {'id': 'all'}).find_all('a')


def parse_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def clean_url(url):
    return url.replace(' ', '%20')


for cat in fetch_titles(inkoopwijzers_str):
    cat_title = cat.text.strip().split(' ')[0]
    cat_href = cat['href']
    print('Category: {}'.format(cat_title))
    print('-------------------')
    for sub in fetch_titles(cat_href):
        sub_title = sub.text.strip().split('(')[0]
        sub_href = sub['href']
        print('-> {}'.format(sub_title))
        for brand in fetch_titles(sub_href):
            brand_title = brand.text.strip().split('(')[0]
            brand_href = brand['href']
            print('=== {}'.format(brand_title))
            for link in fetch_titles(brand_href):
                products_sort = link.text.strip().split('(')[0]
                products_href = link['href']
                payload = {
                    'hoofdstuk': cat_title,
                    'categorie': sub_title,
                    'fabrikant': brand_title,
                    'productsoort': products_sort,
                    'limiet': limit,
                }
                product_content = requests.post(ajax_post_url,
                                                data=payload,
                                                headers={
                                                    'X-Requested-With': 'XMLHttpRequest',
                                                    'referer': clean_url(products_href)
                                                })
                content_table = parse_content(product_content.text).find('table', {'class': 'text'})
                if content_table:
                    for row in content_table.find_all('tr'):
                        item_title = row.find('td', {'class': 'titel2'})
                        item_code = row.find('td', {'class': 'code'})
                        item_amount = row.find('td', {'class': 'aantal'})
                        article_number = ''
                        product_title = ''
                        product_amount = ''
                        if item_title and item_code and item_amount:
                            product_title = item_title.text.strip()
                            article_number = item_code.text.strip()
                            product_amount = item_amount.text.strip()
                            print('Product Title: {}, Article Code: {}, Amount: {}'.format(product_title, article_number, product_amount))
                            data.append([
                                product_title,
                                article_number,
                                product_amount,
                                brand_title,
                                cat_title,
                                sub_title
                            ])

    print('=================================')

with open('inkoopwijzers.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    for row in data:
        try:
            writer.writerow(row)
        except Exception:
            pass
