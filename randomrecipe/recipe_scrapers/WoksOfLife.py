import os
import re
import sys
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger

class WoksOfLife(RecipeScraper):
    def __init__(self):
        super(WoksOfLife, self).__init__()
        self.base_url = "https://thewoksoflife.com/visual-recipe-index/page/{pg_num}/"
        self.max_pg = self.get_max_page_num() if self.scrape_type == 'ALL' else int(self.scrape_type)

    def get_max_page_num(self):
        soup = self.create_soup(self.base_url.format(pg_num = str(1)))
        max_pg = int(re.findall('\d+', soup.find('div',
                                             {'class': 'archive-pagination'}).find_all('li')[-2].text)[0])
        return max_pg

    @task_timer
    def scrape_page(self, pg_num):
        soup = self.create_soup(self.base_url.format(pg_num=str(pg_num)))
        recipes = []
        for article in soup.find('main', {'class':'content flexbox'}).find_all('article'):
            title = article.get('aria-label')
            link = article.find('a')['href']
            recipes.append(('WoksOfLife', title, link))
        return recipes

    def scrape_all_pages(self):
        recipes = []
        for pg_num in range(1, self.max_pg+1):
            logger.info(f"Scraping page number: {str(pg_num)}")
            recipes.extend(self.scrape_page(str(pg_num)))
            # wait for a while
            time.sleep(3)
        return recipes



