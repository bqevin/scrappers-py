# -*- coding: utf-8 -*-
import csv
import urllib2
from bs4 import BeautifulSoup

data = []
adt_str = "https://adt.nl/catalog"


# calls any url and return as bs4 element
def url_parser(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    url = url.replace(' ', '%20')
    req = urllib2.Request(url, headers=hdr)
    content = urllib2.urlopen(req)
    soup = BeautifulSoup(content, 'html.parser')
    return soup


# def get_product(product_url, product_img):
#     item_content = url_parser(product_url)
#     product_title = item_content.find('div', {'class': 'product-name'}).find('h1').text.strip()
#     image_src = product_img
#     brand_name = ''
#     article_number = ''
#     article_number_dental_union = ''
#     fabric_code = ''
#     extra_info = item_content.find('table', {'id': 'product-attribute-specs-table'}).find_all('tr')
#     for single_row in extra_info:
#         row_title = single_row.find('th').text.strip()
#         if row_title == 'Bestelnummer':
#             article_number = single_row.find('td').text.strip()
#         if row_title == 'Leverancier':
#             brand_name = single_row.find('td').text.strip()
#         if row_title == 'Artnr. Dental Union':
#             article_number_dental_union = single_row.find('td').text.strip()
#         if row_title == 'Artnr. Fabrikant':
#             fabric_code = single_row.find('td').text.strip()
#     print('-- ' + product_title)
#     data.append([
#         product_title,
#         image_src,
#         fabric_code,
#         article_number,
#         brand_name,
#         article_number_dental_union,
#         cat_title
#     ])
#
#
# def loop_products_page(url):
#     product_content = url_parser(url)
#     products = product_content.find_all('li', {'class': 'item'})
#     for product in products:
#         product_href = product.find('a')['href']
#         product_img = product.find('a', {'class': 'product-image'}).find('img')
#         if product_img is not None:
#             product_img = product_img['src']
#         # skip ads
#         if product_href == '/speciaal':
#             continue
#         # get products
#         get_product(product_href, product_img)
#
#
# def lookup_pages(url):
#     page_content = url_parser(url)
#     other_page = page_content.find('a', {'class': 'next i-next'})
#     if other_page:
#         loop_products_page(other_page['href'])
#         lookup_pages(other_page['href'])
#
#
# def per_page_products(current_url):
#     #first page in category
#     loop_products_page(current_url)
#     #see pages
#     lookup_pages(current_url)
#     print('===========')


# main homepage
html_content = url_parser(adt_str)
menu = html_content.find('ul', {'class': 'menu--category'})
my_categories = menu.find_all('li', {'class': 'hasDropdown'})

for category in my_categories:
    cat_title = category.select_one('a')
    # cat_href = cat_title['href']
    print(cat_title)


with open('adt.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    for row in data:
        writer.writerow(row)
