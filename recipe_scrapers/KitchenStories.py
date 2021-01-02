import os
import sys
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger


class KitchenStories(RecipeScraper):
    def __init__(self):
        super(KitchenStories, self).__init__()
        self.base_url = "https://www.kitchenstories.com/en/categories/menu?page={pg_num}"
        self.max_pg = self.get_max_page_num() if self.scrape_type == 'ALL' else int(self.scrape_type)

    def get_max_page_num(self):
        soup = self.create_soup(self.base_url.format(pg_num="1"))
        max_pg = max([int(i.find('a')['href'].split("page=")[-1]) for i in soup.find_all('li',{'class':'pagination__arrow'})])
        return max_pg

    @task_timer
    def scrape_page(self, pg_num):
        recipes = []
        soup = self.create_soup(self.base_url.format(pg_num=str(pg_num)))
        for article in soup.find_all('li', {'data-test': 'archive-tile'}):
            title = article.find('a').text
            link = "https://www.kitchenstories.com" + article.find('a')['href']
            image = article.find('img')['src']
            recipes.append(('Kitchen Stories', title, link, image))
        return recipes

    def scrape_all_pages(self):
        recipes = []

        for pg_num in range(1, self.max_pg + 1):
            logger.info(f"Scraping page number: {str(pg_num)}")
            recipes.extend(self.scrape_page(pg_num))
            # wait for a while
            time.sleep(3)
        return recipes

