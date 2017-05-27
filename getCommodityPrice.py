from urllib2 import Request, urlopen
from requests import Session
from lxml import html
import requests
import csv, sys
import pandas as pd

def getCommodityPrice (start_date, end_date, commodity, interval='Daily'):
    '''
    This function will use a simple ajax post call to make session request
    to fetch raw commodity data in xml. 
    
    The CSV writer takes the commodity data from the parser and output
    
    Input:
        start_date: String literal
            Format: 03-03-2016 
            
        end_date: String literal
            Format:03-03-2016
    
        commodity: String literal
            Available options: {gold, silver}
            
        Interval: String (Optional)
            Default: Daily
            Available options: {Daily, Weekly, Monthly}
   
    Output: tuple array of integer
            (mean, variance)
       
    Note: The output can be alter to avoid csv generation simply by keeping a running list
    
    Referene: 
        http://docs.python-requests.org/en/master/user/advanced/ #Usage of Session
        https://stackoverflow.com/questions/3030487/is-there-a-way-to-get-the-xpath-in-google-chrome #xpath
        https://docs.python.org/2/library/csv.html#writer-objects     #CSV writeable python
    
    '''
    default_referer = 'https://www.investing.com/commodities/'
    ajax_endpoint = 'https://www.investing.com/instruments/HistoricalDataAjax'
    xpath_pattern = '//*[@id="curr_table"]/tbody/tr/td/text()'
    user_agent = 'Mozilla/5.0'
    
    #Safe guard against invalid date 
    if len(start_date.split('-')) < 1 or len(end_date.split('-')) < 1:
        raise ValueError('Input date must in month-day-year format')
    
    st_date = '/'.join(start_date.split('-'))
    end_date = '/'.join(end_date.split('-'))
    
    file_extension = '.csv'
    csv_column = ['Date', 'Price', 'Open', 'High', 'Low', 'Vol', 'Change %']
    
    session = Session()
    
    #Safe guard against invalid commodity
    if commodity != 'gold'and commodity != 'silver':
        raise ValueError('Input commodity must be silver or gold')
    
    #AJAX request payload packaging
    response = session.post(
    url=ajax_endpoint,
    data={
        'action': 'historical_data',
        'curr_id': '8830',
        'st_date': start_date,
        'end_date': end_date,
        'interval_sec': interval
    },
    headers={
        'Referer': ''.join([default_referer, commodity, '-historical-data']),
        'user-agent' : xpath_pattern,
        "X-Requested-With": "XMLHttpRequest"
    })
    
    #HTML parser that looks for curr_table similar to the default function
    tree = html.fromstring(response.text)
    data = tree.xpath(xpath_pattern)
    file_name = ''.join([commodity, file_extension])
    
    #CSV generation writing the default column and commodity price
    with open(file_name, 'wb') as f:
        writer = csv.writer(f)
        try:
            writer.writerow(csv_column)
            for i in range(0, len(data), 7):
                row = data[i:i+7]
                writer.writerow(data[i:i+7])
        except csv.Error as e:
            sys.exit('file %s, word %d: %s' % (filename, i, e))        
            
    data = pd.read_csv(file_name, delimiter=',')
    price = data.iloc[:,1].apply(lambda x: float(str(x).replace(',', '')))
    mean = price.mean()
    variance = price.var()
    return commodity, mean, variance