*Python module to get historical data from Yahoo!Finance*
# Yahoo Finance
With the help of this project you can easily extract financial data of companies that are listed at Yahoo!Finance. 
You can save the data as .csv extension or you can setup a simple REST app that returns json file with the saved data
## How to start project
- Open finance.py.
- Choose company or companies in catalog_com. For example `catalog_com = ['PD','ZUO','PINS','ZM','DOCU','CLDR','RUN','PVT.V']`
- Choose period of data. period1 - start, period2 - end, interval - daily, 1 week, 1 month. For example `period1 = 0` (When the value is 0 (zero) we get the maximum period), `period2 = int(time.mktime(datetime.now().date().timetuple()))` (present date),  `interval = '1wk'` (week)
- Save.
- Open db.py
- Substitute your parameters. For example `(conn = psycopg2.connect(dbname='postgres', user='postgres', password='your password', host='localhost'))`. Default it'll be work only local. **Don't use .env file and environment variables**(for example `DB_NAME=os.environ.get("DB_NAME")`)  when you run the script, use only your settings.
- Save.
- open server_fl.py.
- Run.
- Open your browser on http://127.0.0.1:5000/. For example choose the company http://127.0.0.1:5000/?company=pd .
### Required prerequisites :
- Python 3.9.1
- Flask==2.0.1
- requests==2.22.0
- python-dotenv==0.18.0
- PostgreSQL 13
