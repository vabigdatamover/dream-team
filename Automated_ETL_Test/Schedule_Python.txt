#pip install schedule

import shutil, os, glob
import pymongo
from pymongo import MongoClient
import json
import schedule
import time
import pandas as pd

def read_and_move(csv_file):
    df = pd.read_csv(csv_file)
    shutil.move(csv_file, 'test_processed');
    
    return df

def transform(df):
    #Create a HASH
    df['hash'] = pd.Series((hash(tuple(row)) for _, row in df.iterrows()))
    #De-Dupe step
    df_nodupe = df[~df.duplicated()]
    
    return df_nodupe
    

def insert(df):
    df.to_json('ETL_json_file', orient='index')
    
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    client = MongoClient('mongodb://localhost:27017/')
    
    # Create Mongo database named 'etl_db'
    db = client['etl_db']

    # Drop collection if it already exist
    #db.etl_data.drop() # Drop collection if it already exist

    # Create a Mongo collection(table) called 'schedule_test_etl_data'
    collection = db['schedule_test_etl_data']
    
    
    with open('ETL_json_file') as f:
        file_data = json.load(f)
        collection.insert_one(file_data) 
        client.close()

def job():
    print("Performing an ETL process...")
    csv_files = glob.glob('test_input' + '\*.csv')
    dfs = [read_and_move(csv_file) for csv_file in csv_files]
    transformed_dfs = [transform(df) for df in dfs]
    for df in transformed_dfs:
        insert(df)
    print("DONE")
    
    
    #Source Code
    #https://github.com/dbader/schedule  
    
    #Schedule every one minute
schedule.every(1).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)