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
login_action = "https://www.aera-online.de/Asps/Anmelden.asp"
form_username = "pBenutzer"
form_password = "pKennwort"


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


payload = {
    form_username: 'orthoamstelveen',
    form_password: 'Ortho2020',
}
session = requests.Session()
session.get(login_action)
session.post(login_action, data=payload,
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
                'referer': clean_url(aera_online_str+'/Default.asp')
            })


def single_product(url):
    main_page_content = session.get(clean_url(aera_online_str + url))
    page_content = parse_content(main_page_content.text).find('div', {'class': 'objFormularInlineRand'})
    if page_content:
        _title = page_content.find('div', {'class': 'objFormularTitel'})
        td = page_content.find_all('td', {'class': 'objFormularInhalt1'})
        brand_fabric = td[0]
        category = td[1]
        brand_name = ''
        fabric_code = ''
        product_title = ''
        category_title = ''
        if category:
            category_title = category.text.strip().split('\\')[2]
        if brand_fabric:
            brand_fabric = brand_fabric.text.strip()
            try:
                brand_name = brand_fabric.split(',')[0]
            except IndexError:
                brand_name = ''
            try:
                fabric_code = brand_fabric.split(':')[1]
            except IndexError:
                fabric_code = ''
        if _title:
            product_title = _title.text.strip()
        #find the henry schein loop
        for competitor in parse_content(main_page_content.text).find('div', {'class': 'objKarteiInhalt'}).find_all('tr', {'class': 'objTabelle2Block'}):
            text_data = competitor.find('td', {'class': 'objTabelle2BlockLinks'}).text.strip()
            if "Henry Schein Dental Depot GmbH" in text_data:
                href_data = competitor.find('td', {'class': 'objTabelle2BlockRechts'})
                href_data = href_data.find('a')['href']
                hc_content = parse_content(session.get(clean_url(aera_online_str + href_data)).text)
                hc_content = hc_content.find('table', {'class': 'objFormular'})
                for hc_row in hc_content.find_all('tr'):
                    if "Bestellnummer" in hc_row.find('td', {'class': 'objFormularBeschriftung'}).text.strip():
                        hc_article_code = hc_row.find('td', {'class': 'objFormularInhalt1'}).text.strip()
                        print('Category: {}, Product: {}, Fabric Code: {}, Article Code: {}'.format(category_title, product_title,fabric_code, hc_article_code))
                        data.append([
                            product_title,
                            brand_name,
                            hc_article_code,
                            fabric_code,
                            category_title,
                        ])
                break


def loop_products_list(url):
    product_content = url_parser(aera_online_str + url).find('div', {'class': 'objTabelle2'})
    product_content.find('table').find('tbody')
    if product_content:
        for row_ in product_content.find_all('tr', {'class': 'objTabelle2'}):
            product_href = row_.find('td').find('a')
            product_title = product_href.find('img')
            if product_href:
                product_title = product_title['title']
                product_href = product_href['href']
                single_product(product_href)


def loop_cat_tables(url):
    _content = url_parser(aera_online_str + url).find('table', {'class': 'ContentContainerTransparent'})
    if _content:
        important_content = _content.find('tbody')
        if important_content:
            for _row in important_content.find_all('tr', {'class': 'ContentContainerTransparent'}):
                for _col in _row.find_all('td'):
                    if _col.find('a') is None:
                        continue
                    _title = _col.text.strip()
                    _href = _col.find('a')
                    if _href is not None:
                        _href = _href['href']
                    print('--> {} : {}'.format(_title, _href))
                    loop_cat_tables(_href)
    else:
        loop_products_list(url)


html_content = url_parser(aera_online_catalog)
html_content = html_content.find('table', {'class': 'ContentContainerTransparent'}).find('tbody')
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
        loop_cat_tables(cat_href)

    print('=================================')

with open('aera_online.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    for row in data:
        try:
            writer.writerow(row)
        except Exception:
            pass
