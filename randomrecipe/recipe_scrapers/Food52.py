import re
import os
import sys
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger


class Food52(RecipeScraper):
    def __init__(self):
        super(Food52, self).__init__()
        self.base_url = "https://food52.com/recipes/search?o=newest&page={pg_num}&tag=test-kitchen-approved"
        self.max_pg = self.get_max_page_num() if self.scrape_type == 'ALL' else int(self.scrape_type)

    def get_max_page_num(self):
        soup = self.create_soup(self.base_url.format(pg_num=str(1)))
        max_pg = max(
            [int(re.findall(r"\d+", i.text)[0]) for i in soup.find('div', {'role': 'navigation'}).find_all('a') if
             len(re.findall(r"\d+", i.text)) > 0])
        return max_pg

    @task_timer
    def scrape_page(self, pg_num):
        soup = self.create_soup(self.base_url.format(pg_num=str(pg_num)))
        recipes = []
        for article in soup.find_all('div', {'class': 'photo-block'}):
            title = article.find('a')['title']
            link = f"https://food52.com/{article.find('a')['href']}"
            recipes.append(('Food52', title, link))
        return recipes

    def scrape_all_pages(self):
        recipes = []

        for pg_num in range(1, self.max_pg + 1):
            logger.info(f"Scraping page number: {str(pg_num)}")
            recipes.extend(self.scrape_page(pg_num))
            # wait for a while
            time.sleep(3)
        return recipes
