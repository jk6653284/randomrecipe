import os
import sys
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger


class JustOneCB(RecipeScraper):
    def __init__(self):
        super(JustOneCB, self).__init__()
        self.base_url = "https://www.justonecookbook.com/recipes"
        self.max_pg = self.get_max_page_num() if self.scrape_type == 'ALL' else int(self.scrape_type)

    def get_max_page_num(self):
        soup = self.create_soup(f"{self.base_url}/page/1")
        max_pg = max([int(i.text) for i in soup.find_all('a', {'class': 'page-numbers'}) if i.text.isdigit()])
        return max_pg

    @task_timer
    def scrape_page(self, pg_num):
        soup = self.create_soup(f"{self.base_url}/page/{str(pg_num)}")
        recipes = []
        for article in soup.find_all('div', {'class': 'featured-image'}):
            link = article.find('a')['href']
            title = article.find('a')['title']
            image = article.find('a').find('img')['src']
            recipes.append(('Just One CookBook', title, link, image))
        return recipes

    def scrape_all_pages(self):
        recipes = []

        for pg_num in range(1, self.max_pg + 1):
            logger.info(f"Scraping page number: {str(pg_num)}")
            recipes.extend(self.scrape_page(pg_num))
            # wait for a while
            time.sleep(3)
        return recipes
