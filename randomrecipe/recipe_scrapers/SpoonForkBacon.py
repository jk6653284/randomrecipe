import os
import sys
import re
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger


class SpoonForkBacon(RecipeScraper):
    def __init__(self):
        super(SpoonForkBacon, self).__init__()
        self.base_url = "https://www.spoonforkbacon.com/blog/page/{pg_num}"
        self.max_pg = self.get_max_page_num() if self.scrape_type == 'ALL' else int(self.scrape_type)

    def get_max_page_num(self):
        soup = self.create_soup(self.base_url.format(pg_num='1'))
        max_pg = re.findall(r"\d+",soup.find('div',
                                             {'class':'archive-pagination'}).find_all('li')[-2].text)[0]
        return int(max_pg)

    @task_timer
    def scrape_page(self, pg_num):
        soup = self.create_soup(self.base_url.format(pg_num=str(pg_num)))
        recipes = []
        for article in soup.find_all('recipe'):
            title = article.find('h2').find('a').text
            link = article.find('h2').find('a')['href']
            recipes.append(('Spoon Fork Bacon', title, link))
        return recipes

    def scrape_all_pages(self):
        recipes = []

        for pg_num in range(1, self.max_pg + 1):
            logger.info(f"Scraping page number: {str(pg_num)}")
            recipes.extend(self.scrape_page(pg_num))
            # wait for a while
            time.sleep(3)
        return recipes