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


def lookup_pages(url):
    page_content = url_parser(url)
    other_page = page_content.find('a', {'class': 'next i-next'})
    if other_page:
        loop_products_page(other_page['href'])
        lookup_pages(other_page['href'])


def per_page_products(current_url):
    #first page in category
    loop_products_page(current_url)
    #see pages
    lookup_pages(current_url)


# main homepage
html_content = url_parser(dental_union_str)
my_categories = html_content.find_all("li", {"class": "item"})


for category in my_categories:
    cat_title = category.text.strip()
    cat_href = dental_union_str + category.find('a')['href']
    print(cat_title)
    per_page_products(cat_href)

with open('dental_union.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    for row in data:
        writer.writerow(row)
