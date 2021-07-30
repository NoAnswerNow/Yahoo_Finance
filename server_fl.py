from flask import Flask, request
import psycopg2
import logging
from db import create_db, create_tables, write_data, get_historical_data_by_company_name
from finance_content import get_data, companiaes_data

print('Starting server...')

app = Flask(__name__)


with app.app_context():
    create_db()
    create_tables()
    companiaes_data()

@app.route("/")
def data_yahoo():
    app.logger.info(request.args.get('company'))
    comp_name = request.args.get('company')
    if comp_name is not None:
        results = get_historical_data_by_company_name(comp_name)

        return str(results)
    else:
        return('404')    

    
if __name__=="__main__" :
    app.run(debug=True)    