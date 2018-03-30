# -*- coding: utf-8 -*-
import csv

data = [[
    'Kevin Product',
    'http://localhost/image',
    '2NLJ9',
    '0000678TGS',
    '3M',
    'Stimulant',
    'test stimulant',
    ''
], [
    'John Product',
    'http://localhost/image',
    '3NLJ9',
    '0000678TGS',
    '4M',
    'Cooler',
    'test cooler',
    'has under hidden'
]]

with open('mailmix.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    for row in data:
        writer.writerow(row)
