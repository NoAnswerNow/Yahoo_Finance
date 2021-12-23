from flask import Flask, request, render_template, url_for
import psycopg2
import logging
from db import create_db, create_tables, write_data, get_historical_data_by_company_name
from finance_content import get_data, companiaes_data
from new_company import get_new_company


print('Starting server...')
app = Flask(__name__)
with app.app_context():
    create_db()
    create_tables()
    companiaes_data()


@app.route("/", methods=['POST'])
def data_yahoo():
    comp_name = request.form.get("nm")
    comp_name = comp_name.upper()
    results = get_historical_data_by_company_name(comp_name)
    if results :
        return render_template("index.html", value=(results))
    elif not results  :
        #if we have the empty list get the data of new company and write it to db
        get_new_company(comp_name)
        return render_template("index.html", value=(results))
    else:
        return render_template("index.html", value='error 404')
if __name__=="__main__" :
    app.run(debug=True)