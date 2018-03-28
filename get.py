from bs4 import BeautifulSoup
import urllib2

mailmix_str = "http://webshop.mailmix.nl/catalog/category/"

content = urllib2.urlopen(mailmix_str).read()

soup = BeautifulSoup(content)

print soup.prettify()