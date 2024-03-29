import os
import sys
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger

class HalfBakedHarvest(RecipeScraper):
    def __init__(self):
        super(HalfBakedHarvest, self).__init__()
        self.base_url = "https://www.halfbakedharvest.com/recipes/?_paged={pg_num}"
        self.max_pg = self.get_max_page_num() if self.scrape_type == 'ALL' else int(self.scrape_type)

    def get_max_page_num(self):
        try:
            soup = self.create_soup(self.base_url.format(pg_num = str(1)))
            max_pg = max([int(pg.text) for pg in soup.find_all('a', {'class': 'page-numbers'}) if pg.text.isnumeric()])
            return max_pg
        except Exception as e:
            print(f"Cannot scrape pagination, defaulting to 20 pages")


    @task_timer
    def scrape_page(self, pg_num):
        soup = self.create_soup(self.base_url.format(pg_num=str(pg_num)))
        recipes = []
        for recipe in soup.find_all('article',{'class':'post-summary primary'}):
            title = recipe.find('h3').text
            link = recipe.find('h3').find('a')['href']
            recipes.append(('HalfBakedHarvest', title, link))
        return recipes

    def scrape_all_pages(self):
        recipes = []
        for pg_num in range(1, self.max_pg+1):
            logger.info(f"Scraping page number: {str(pg_num)}")
            recipes.extend(self.scrape_page(str(pg_num)))
            # wait for a while
            time.sleep(10)
        return recipes