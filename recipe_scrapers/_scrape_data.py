"""
Scrape url of recipes from corresponding websites
"""
# imports
from functools import wraps
import datetime as dt
import os
import sqlite3
import sys

from bs4 import BeautifulSoup
import requests
from retry import retry

import yaml
configs = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), '../config.yml')))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger


# decorator to measure how long the scraping works for
def task_timer(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        t0 = dt.datetime.now()
        print(f"{func.__name__} started at {t0}")
        result = func(*args,**kwargs)
        print(f"{func.__name__} finished in {(dt.datetime.now() - t0)/60} minutes.")
        return result
    return wrapper

class RecipeScraper:
    """
    recipe scraper class as scraping itself is all the same
    and exporting is the same
    retrieving different parts is the different part
    """
    def __init__(self,configs=configs):
        """

        :param configs:
        :param
        """
        self.scrape_type = configs['SCRAPE_TYPE']
        self.table_schema = configs['TABLE_SCHEMA']
        self.table_name = configs['TABLE_NAME']

    @retry(BaseException,tries=3,delay=0.5)
    def create_soup(self,url,headers=None):
        """
        Returns beautiful soup object
        :param url:
        :return:
        """
        if headers:
            req = requests.get(url,headers=headers)
        else:
            req = requests.get(url)
        try:
            logger.info(f"Soup object created for {url}")
            soup = BeautifulSoup(req.text,'lxml')
            return soup
        except BaseException:
            logger.error(f"Error happened", exc_info = True)

    def db_connect(self):
        conn = sqlite3.connect(self.table_schema)
        cursor = conn.cursor()
        return conn, cursor

    @task_timer
    def export_data(self,data):
        conn, cursor = self.db_connect()
        logger.info(f"Inserting {len(data)} rows into {self.table_schema}.{self.table_name}")
        insert_query = f"INSERT OR IGNORE INTO {self.table_name} VALUES ({','.join(['?'] * len(data[0]))});"
        try:
            cursor.executemany(insert_query, data)
            conn.commit()
            conn.close()
        except BaseException:
            logger.error(f"Error happened", exc_info=True)
