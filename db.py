import psycopg2
import os
import sys
from os.path import join, dirname
from dotenv import load_dotenv
import json


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
DB_NAME=os.environ.get("DB_NAME")
DB_USER=os.environ.get("DB_USER")
DB_PASSWORD=os.environ.get("DB_PASSWORD")
DB_HOST=os.environ.get("DB_HOST")
DB_DEFAULT_NAME=os.environ.get("DB_DEFAULT_NAME")
print('Connecting to db...')


def create_db():
    #Creating a database
    conn = None
    try:
        conn = psycopg2.connect(dbname=DB_DEFAULT_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        conn.autocommit = True
        cur = conn.cursor()
        print('Creating db yahoo_finance...')
        cur.execute("DROP DATABASE IF EXISTS yahoo_finance")
        #Preparing query to create a database
        sql = '''CREATE database yahoo_finance''';
        cur.execute(sql)
        cur.execute("SELECT version()")
        version = cur.fetchone()[0]
        print(version)
    except psycopg2.DatabaseError as e :
        print(f'Error {e}')
        #sys.exit(1)
    finally:
        if conn:
            conn.close()


def create_tables():
    print('Creating tables...')
    conn = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS companies, historical_data")
        sql = '''CREATE TABLE companies (
        id SERIAL PRIMARY KEY ,
        name TEXT NOT NULL
        );
        CREATE TABLE historical_data(
        id SERIAL PRIMARY KEY ,
        comp_id INTEGER,
        FOREIGN KEY(comp_id) REFERENCES companies(id),
        Date date  NOT NULL,
        Open NUMERIC NOT NULL,
        High NUMERIC NOT NULL,
        LOW NUMERIC NOT NULL,
        Close NUMERIC NOT NULL,
        AdjClose NUMERIC NOT NULL,
        Volume NUMERIC NOT NULL
        );
        '''
        cur.execute(sql)
        print('Successfully')
    except psycopg2.DatabaseError as e:
        print(f'Erorr {e}')
        #sys.exit(1)
    finally:
        if conn:
            cur.close()
            conn.close()


def write_data(file_name, company_name):
    conn = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        conn.autocommit = True
        cur = conn.cursor()
        id_comp=cur.execute(
            "INSERT INTO companies (name) VALUES ('{}') RETURNING id".format(company_name)  
            )
        id_comp = cur.fetchone()[0]
        with open(file_name) as f:
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


def get_historical_data_by_company_name(comp_name):
    conn = None
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT * FROM historical_data WHERE comp_id =(SELECT id FROM companies WHERE name=UPPER('{}'))".format(comp_name))
        results = []
        columns = [column[0] for column in cur.description]
        for row in cur.fetchall():
            json_row = json.dumps(row, ensure_ascii=False,default=str).replace(
            ']', '').replace('[', '').split(',')
            results.append(dict(zip(columns,json_row)))
    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        #sys.exit(1)
    finally:
        if conn:
            cur.close()
            conn.close()
    return results