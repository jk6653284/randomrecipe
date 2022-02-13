import os
import sys
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger


class SeriousEats(RecipeScraper):
    def __init__(self):
        super(SeriousEats, self).__init__()
        self.base_url = "https://www.seriouseats.com/recipes/topics/meal?page={pg_num}&sort=latest#recipes"
        self.max_pg = self.get_max_page_num() if self.scrape_type == 'ALL' else int(self.scrape_type)

    def get_max_page_num(self):
        soup = self.create_soup(self.base_url.format(pg_num=str(1)))
        max_pg = max([int(p.text) for p in soup.find('div',{'class':'ui-pagination-jump-links'}).find_all('a')])
        return max_pg

    @task_timer
    def scrape_page(self,pg_num):
        recipes = []
        soup = self.create_soup(self.base_url.format(pg_num=str(pg_num)))

        for article in soup.find_all('section', {'class': 'block block-primary block-no-nav'})[0].find_all('article'):
            link = article.find('a')['href']
            title = article.find('a', {'class': 'o-link-wrapper'}).text
            recipes.append(('Serious Eats', title, link))
        return recipes

    def scrape_all_pages(self):
        recipes = []

        for pg_num in range(1,self.max_pg + 1):
            logger.info(f"Scraping page number: {str(pg_num)}")
            recipes.extend(self.scrape_page(pg_num))
            # wait for a while
            time.sleep(3)
        return recipes
