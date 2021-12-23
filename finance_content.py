import requests
import time
import datetime
from datetime import datetime
from random import randint
from time import sleep
import csv
from pathlib import Path
from db import write_data


Path("./company_data").mkdir(exist_ok=True)
# in task we have PVTL company but it's defunct company. I'll scrap PVT.V company
# 'PD', 'ZUO', 'PINS', 'ZM', 'PVT.V', 'DOCU', 'CLDR' ,'RUN'] # list of companies
catalog_com = ['PD','ZUO']
#catalog_com = ['PD','ZUO','PINS','ZM','DOCU','CLDR','RUN','PVT.V']


def get_data(company):
    """
    Function used to get a  text from a Beautiful Soup
     object
    """
    catalog = {'company': company}  # choose the company
    # get MAX period
    period1 = 0 # you can choose any date. When the value is 0 (zero) we get the maximum period
    period2 = int(time.mktime(datetime.now().date().timetuple()))  # get the last date(present date)
    interval = '1wk'  # (1d, 1 wk, 1m) can choose frequency: day, week or month
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{company}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
                }
    res = requests.get(url, headers=headers)
    if res.status_code == 200 :
        return res.text
    else:
        return None


# get content for all companies
def companiaes_data():
        company_data = []
        for firm in catalog_com :
            company_data.append(get_data(firm))
            print('Download :', firm, 'company')
            time.sleep(randint(5, 25)) # change the frequency of requests
            # save data to .csv file
            data_file = open("./company_data/{}.csv".format(firm), "w")
            for line in company_data:
                data_file.write(line)
            data_file.close()
            print('CSV file saved')
            company_data = []
        #Write to DB
        print('Recording to DB...')
        for firm in catalog_com:
            write_data("./company_data/{}.csv".format(firm), firm)
        print('Successfully')







