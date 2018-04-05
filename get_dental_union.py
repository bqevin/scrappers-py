# -*- coding: utf-8 -*-
import csv
import urllib2
from bs4 import BeautifulSoup

data = []
dental_union_str = "https://shop.dentalunion.nl"


# calls any url and return as bs4 element
def url_parser(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    url = url.replace(' ', '%20')
    req = urllib2.Request(url, headers=hdr)
    content = urllib2.urlopen(req)

    soup = BeautifulSoup(content, 'html.parser')
    return soup


def loop_products_page(url):
    product_content = url_parser(url)
    products = product_content.find_all('li', {'class': 'item'})
    for product in products:
        product_href = product.find('a')['href']
        # skip ads
        if product_href == '/speciaal':
            continue
        print('--' + product_href)
        # get products
        # data.append([
        #     product_title,
        #     image_src,
        #     fabric_code,
        #     article_number,
        #     brand_name,
        #     cat_title,
        #     sub_title,
        # ])


# main homepage
html_content = url_parser(dental_union_str)
my_categories = html_content.find_all("li", {"class": "item"})


for category in my_categories:
    cat_title = category.text.strip()
    cat_href = dental_union_str + category.find('a')['href']
    print(cat_title)
    loop_products_page(cat_href)
    cat_content = url_parser(cat_href)
    pages = cat_content.find('div', {'class': 'pages'})
    if pages:
        pages_links = pages.find_all('li')
        stage = 0
        for page_link in pages_links:
            stage = stage + 1
            if stage >= 2:
                page_href = page_link.find('a')['href']
                loop_products_page(page_href)

with open('dental_union.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    for row in data:
        writer.writerow(row)
