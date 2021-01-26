import os
import sys
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger

class SweetPillarFood(RecipeScraper):
    def __init__(self):
        super(SweetPillarFood, self).__init__()
        self.base_url = "https://www.sweetpillarfood.com/recipeindex/page/{pg_num}/"
        self.max_pg = self.get_max_page_num()

    def get_max_page_num(self):
        soup = self.create_soup(self.base_url.format(pg_num=str(1)))
        max_pg = max([int(pg.text) for pg in soup.find('div', {'class':'nav-links'}).find_all('a',{'class':'page-numbers'}) if pg.text.isnumeric()])
        return max_pg

    @task_timer
    def scrape_page(self, pg_num):
        soup = self.create_soup(self.base_url.format(pg_num=str(pg_num)))
        recipes = []
        for recipe in soup.find_all('article', {'class': 'simple-grid'}):
            title = recipe.get('aria-label')
            link = recipe.find('a')['href']
            try:
                image = recipe.find('img')['src']
            except Exception as e:
                image = ""
            recipes.append(('SweetPillarFood', title, link, image))
        return recipes

    def scrape_all_pages(self):
        recipes = []
        for pg_num in range(1,self.max_pg+1):
            logger.info(f"Scraping page number: {str(pg_num)}")
            recipes.extend(self.scrape_page(str(pg_num)))
            # wait for a while
            time.sleep(3)
        return recipes
