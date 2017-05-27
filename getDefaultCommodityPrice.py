from urllib2 import Request, urlopen
from requests import Session
from lxml import html
import requests
import csv, sys
import pandas as pd

def getDefaultCommodityPrice ():
    '''
    Default scraper that fetch from two end point (gold and silver)
    Uses session and xpath to fetch data from the end point
    
    Output: Return void
        Two files in the ./ with gold.xlsx and silver.xlsx
    '''
    commodities = ['gold', 'silver']
    hist_substring = '-historical-data'
    file_extension = '.csv'
    csv_column = ['Date', 'Price', 'Open', 'High', 'Low', 'Vol', 'Change %']
    end_point = 'https://www.investing.com/commodities/'
    xpath_pattern = '//*[@id="curr_table"]/tbody/tr/td/text()'
    header = {'User-Agent': 'Mozilla/5.0'}

    for commodity in commodities:
        req = Request(''.join([end_point,commodity,hist_substring]), headers=header)
        webpage = urlopen(req).read()
        tree = html.fromstring(webpage)
        data = tree.xpath(xpath_pattern)
        filename = ''.join([commodity, file_extension])
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(csv_column)
            for i in range(0, len(data), 7):
                writer.writerow(data[i:i+7])