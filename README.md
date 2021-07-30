# Yahoo Finance
With the help of this project you can easily extract financial data of companies that are listed at Yahoo!Finance. 
You can save the data as .csv extension or you can setup a simple REST app that returns json file with the saved data
## How to start project
- Open finance_content.py
- Choose company or companies in catalog_com. For example catalog_com = ['PD','ZUO','PINS','ZM','DOCU','CLDR','RUN','PVT.V']
- Choose period of data. period1 - start, period2 -end, interval - daily, 1 week, 1 month. For example period1 = 0 (When the value is 0 (zero) we get the maximum period),  period2 = int(time.mktime(datetime.now().date().timetuple())) (present date),  interval = '1wk' (1 week).
- Save.
- Open db.py
- Substitute your parameters. For example (dbname='postgres', user='postgres', password='your password', host='localhost').Default it'll be work only local.
- Save
- Open server_fl.py
- Run 
### Required prerequisites:
- Python 3.9.1
- Flask==2.0.1
- psycopg2==2.9.1
- requests==2.22.0
- python-dotenv==0.18.0
