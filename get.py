# -*- coding: utf-8 -*-
import csv
import urllib2
from bs4 import BeautifulSoup
import sys

data = []
mail_mix_str = "http://webshop.mailmix.nl/catalog/category/"


# calls any url and return as bs4 element
def url_parser(url):
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    return soup


html_content = url_parser(mail_mix_str)

my_categories = html_content.find_all("li", {"class": "level0"})


# Get products in any category provided a URL
def products_loop(url):
    my_products = url_parser(url)
    for item in my_products.find_all('div', {'class': 'item-container'}):
        item_href = item.find('a')['href']
        item_title = item.find('a')['title']
        single_item = url_parser(item_href)
        product_desc = single_item.find('h1').text.strip()
        image_check = single_item.find('p', {'class': 'product-image'})
        image_src = ''
        if image_check is not None:
            image_src = image_check.find('img')['src']
        check_fabric_code = single_item.find('p', {'class': 'short-description'})
        brand_name = product_desc.split(" ")[0]
        fabric_code = ''
        if check_fabric_code is not None:
            fabric_code = check_fabric_code.text
        # check_article_number = single_item.find('table', {'class': 'data-table'}).find('td', {'class': 'data last'})
        # article_number = ''
        # if check_article_number is not None:
        #     article_number = check_article_number.text
        print(image_src)
        data.append([
            product_desc,
            image_src,
            fabric_code,
            # article_number,
            brand_name,
            cat_title,
            sub_title,
            under_title
        ])


def get_products(url):
    this_page = url_parser(url)
    #initial first page
    print('===== Now on page 1')
    products_loop(url)

    if this_page.find('div', {'class': 'pages'}):
        pages = this_page.find('div', {'class': 'pages'}).find_all('li')
        stage = 0
        for page in pages:
            stage = + 1
            # skip using href in first loop
            if stage >= 2:
                current_page_url = page.find('a')['href']
                products_loop(current_page_url)
                print('===== Now on page ' + stage)


for category in my_categories:
    cat_title = category.find('a').text.strip()
    sub_cat = category.find_all('li', {'class': 'level1'})
    print(cat_title)

    # Loop through the subcategories
    for sub in sub_cat:
        sub_href = sub.find('a')['href']
        sub_title = sub.find('a').text.strip()
        under_title = ''
        print(sub_title)

        # find products -> single product
        get_products(sub_href)

        # if there is under cat - go step deeper
        if sub.find('ul', {'class': 'level1'}):
            under_sub = sub.find_all('li', {'class': 'level2'})
            for _under in under_sub:
                under_href = _under.find('a')['href']
                under_title = _under.find('a').text.strip()
                print(under_title)

                # find products -> single product
                get_products(under_href)
    print('----------------')

with open('mailmix.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
writer.writerow(data)
