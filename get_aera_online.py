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
aera_online_str = "https://www.aera-online.de"
aera_online_catalog = "https://www.aera-online.de/Asps/Katalog.asp"


# calls any url and return as bs4 element
def url_parser(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(clean_url(url), headers=hdr)
    content = urllib2.urlopen(req)
    return parse_content(content)


def parse_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def clean_url(url):
    return url.replace(' ', '%20')


def loop_cat_tables(url):
    page_content = url_parser(aera_online_str + url)
    important_content = page_content.find('table', {'class': 'ContentContainerTransparent'})
    product_content = page_content.find('div', {'class': 'objTabelle2'})
    if product_content:
        product_content = product_content.find('table')
        product_content = product_content.find('tbody')
        print(product_content)
        # for rows in product_content.find_all('tr'):
        #         details = rows.select('td:nth-of-type(1)')
        #         product_title = details.find('a', {'class': 'LinkProduct'}).text.strip()
        #         print('===== {}'.format(product_title))
    #TODO: recurse if pages
    if important_content:
        important_content = page_content.find('tbody')
        if important_content:
            for row_ in important_content.find_all('tr', {'class': 'ContentContainerTransparent'}):
                for col in row_.find_all('td'):
                    if col.find('a') is None:
                        continue
                    title = col.text.strip()
                    href = col.find('a')
                    if href is not None:
                        href = href['href']
                    print('--> {}'.format(title, href))
                    loop_cat_tables(href)


html_content = url_parser(aera_online_catalog).find('table', {'class': 'ContentContainerTransparent'}).find('tbody')
for row in html_content.find_all('tr', {'class': 'ContentContainerTransparent'}):
    for cat in row.find_all('td'):
        if cat.find('a') is None:
            continue
        cat_title = cat.text.strip()
        cat_href = cat.find('a')
        if cat_href is not None:
            cat_href = cat_href['href']
        print('---------------------------------')
        print('Category: {}'.format(cat_title))
        print('---------------------------------')
        #TODO: Before looking for table, check if products are there already. Need a recursive here
        loop_cat_tables(cat_href)

    #     print('-> {}'.format(sub_title))
    #     for brand in fetch_titles(sub_href):
    #         brand_title = brand.text.strip().split('(')[0]
    #         brand_href = brand['href']
    #         print('=== {}'.format(brand_title))
    #         for link in fetch_titles(brand_href):
    #             products_sort = link.text.strip().split('(')[0]
    #             products_href = link['href']
    #             payload = {
    #                 'hoofdstuk': cat_title,
    #                 'categorie': sub_title,
    #                 'fabrikant': brand_title,
    #                 'productsoort': products_sort,
    #                 'limiet': limit,
    #             }
    #             product_content = requests.post(ajax_post_url,
    #                                             data=payload,
    #                                             headers={
    #                                                 'X-Requested-With': 'XMLHttpRequest',
    #                                                 'referer': clean_url(products_href)
    #                                             })
    #             content_table = parse_content(product_content.text).find('table', {'class': 'text'})
    #             if content_table:
    #                 for row in content_table.find_all('tr'):
    #                     item_title = row.find('td', {'class': 'titel2'})
    #                     item_code = row.find('td', {'class': 'code'})
    #                     item_amount = row.find('td', {'class': 'aantal'})
    #                     article_number = ''
    #                     product_title = ''
    #                     product_amount = ''
    #                     if item_title and item_code and item_amount:
    #                         product_title = item_title.text.strip()
    #                         article_number = item_code.text.strip()
    #                         product_amount = item_amount.text.strip()
    #                         print('Product Title: {}, Article Code: {}, Amount: {}'.format(product_title, article_number, product_amount))
    #                         data.append([
    #                             product_title,
    #                             article_number,
    #                             product_amount,
    #                             brand_title,
    #                             cat_title,
    #                             sub_title
    #                         ])

    # print('=================================')

with open('aera_online.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    for row in data:
        try:
            writer.writerow(row)
        except Exception:
            pass
