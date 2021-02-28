import os
import sys
import re
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger

class Lacucina(RecipeScraper):
    def __init__(self):
        super(Lacucina, self).__init__()
        self.base_url = "https://www.lacucinaitaliana.com/recipes/pag/{pg_num}"
        self.max_pg = self.get_max_page_num() if self.scrape_type == 'ALL' else int(self.scrape_type)

    def get_max_page_num(self):
        soup = self.create_soup(self.base_url.format(pg_num='1'))
        max_pg = int(re.findall(r"[0-9]+",
                            soup.find('a',{'aria-label':'Go to last page'}).get('href'))[0]
                     )
        return max_pg

    @task_timer
    def scrape_page(self,pg_num):
        soup = self.create_soup(self.base_url.format(pg_num=str(pg_num)))
        recipes = []
        for article in soup.find_all('article',{'class':'article-item-single'}):
            link = f"https://www.lacucinaitaliana.com{article.find('a')['href']}"
            title = article.find('a')['name']
            image = article.find('img')['data-src']
            recipes.append(('La Cucina Italiana',title,link,image))

        return recipes

    def scrape_all_pages(self):
        recipes = []
        for pg_num in range(1,self.max_pg+1):
            logger.info(f"Scraping page number: {str(pg_num)}")
            recipes.extend(self.scrape_page(pg_num))
            # wait for a while
            time.sleep(3)
        return recipes

