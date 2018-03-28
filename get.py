# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

mailmix_str = "http://webshop.mailmix.nl/catalog/category/"
content = urllib2.urlopen(mailmix_str).read()
soup = BeautifulSoup(content, 'html.parser')

data = []
my_categories = soup.find_all("li", {"class": "level0"})

# data.append((things))
# with open(‘index.csv’, ‘a’) as csv_file:
#     writer = csv.writer(csv_file)
# writer.writerow([name, price, datetime.now()])

for category in my_categories:
    print(category.find('a').text.strip())

