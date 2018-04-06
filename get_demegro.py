# -*- coding: utf-8 -*-
import csv
import urllib2
from bs4 import BeautifulSoup

data = []
demegro_str = "https://demegro.nl/"


# calls any url and return as bs4 element
def url_parser(url):
    url = url.replace(' ', '%20')
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    return soup


# main homepage
html_content = url_parser(demegro_str)
my_categories = html_content.find_all("a", {"class": "hoofdstuk"})

stage = 0
for category in my_categories:
    stage = stage + 1
    # skip first 2
    if stage >= 3:
        cat_title = category.text.strip()
        cat_href = category['href']
        print(cat_title)
        sub_cat_content = url_parser(cat_href)
        sub_cat = sub_cat_content.find_all('a', {'class': 'categorie'})
        for sub in sub_cat:
            sub_title = sub.text.strip()
            sub_href = sub['href']
            print('--' + sub_title)
            under_sub_cat_content = url_parser(sub_href)
            under_sub_cat = under_sub_cat_content.find_all('span', {'class': 'hide'})
            for under_sub in under_sub_cat:
                under_sub_href = under_sub.text.strip()
                under_sub_href = sub_href + '/' + under_sub_href
                # print(under_sub_href)
                product_content = url_parser(under_sub_href)
                products = product_content.find_all('div', {'class': 'article'})
                brand_name = product_content.find('label')
                if brand_name is not None:
                    brand_name = brand_name.text.strip()
                    brand_name.encode('ascii', 'ignore').decode('ascii')
                for product in products:
                    product_title = product.find('h2').text.strip()
                    product_title.encode('ascii', 'ignore').decode('ascii')
                    article_number_element = product.find('span', {'class': 'code'})
                    article_number = article_number_element.text.strip()
                    fabric_code = article_number_element.find_next_siblings('span', {'class': 'code'})[0].find('span', {'class': 'rightclick'})
                    if fabric_code is not None:
                        fabric_code = fabric_code.text.strip()
                        fabric_code.encode('ascii', 'ignore').decode('ascii')
                    image_src = product.find('div', {'class': 'imgHolder'}).find('img')
                    if image_src is not None:
                        image_src = image_src['src']
                    print(product_title)
                    data.append([
                        product_title,
                        image_src,
                        fabric_code,
                        article_number,
                        brand_name,
                        cat_title,
                        sub_title,
                    ])


with open('d_.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    for row in data:
        try:
            writer.writerow(row)
        except Exception:
            pass
