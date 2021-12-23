from finance_content import get_data
import csv
from flask import Flask, request
import psycopg2
import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv
from db import get_historical_data_by_company_name
import requests


app = Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
DB_NAME=os.environ.get("DB_NAME")
DB_USER=os.environ.get("DB_USER")
DB_PASSWORD=os.environ.get("DB_PASSWORD")
DB_HOST=os.environ.get("DB_HOST")
DB_DEFAULT_NAME=os.environ.get("DB_DEFAULT_NAME")


#get the data of new company and write to db
def get_new_company(comp_name):
    results = get_historical_data_by_company_name(comp_name)
    new_comp = get_data(comp_name)
    if new_comp is None:
        return None
    else :
        data_file = open("./company_data/{}.csv".format(comp_name), "w")
        for line in new_comp:
            data_file.write(line)
        data_file.close()
        conn = None
        try:
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
            conn.autocommit = True
            cur = conn.cursor()
            id_comp=cur.execute("INSERT INTO companies (name) VALUES ('{}') RETURNING id".format(comp_name))  
            id_comp = cur.fetchone()[0]
            with open("./company_data/{}.csv".format(comp_name)) as f:
                content = f.readlines()
                content = [x.strip() for x in content]
                content.pop(0)
                for row in content:
                    result = [x.strip() for x in row.split(',')]
                    cur.execute(
                        "INSERT INTO historical_data (Date,Open,High,Low,Close,AdjClose,Volume,comp_id) VALUES ('{}', {}, {}, {},{},{},{},{})".format(result[0], result[1], result[2], result[3], result[4], result[5], result[6],id_comp))
        except psycopg2.DatabaseError as e:
            print(f'Error {e}')
            #sys.exit(1)
        finally:
            if conn:
                cur.close()
                conn.close()
