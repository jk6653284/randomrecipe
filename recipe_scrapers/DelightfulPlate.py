import os
import sys
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger


class DelightfulPlate(RecipeScraper):
    def __init__(self):
        super(DelightfulPlate, self).__init__()
        self.base_url = "https://delightfulplate.com/vietnamese-recipes/?_page={pg_num}"
        self.max_pg = self.get_max_page_num() if self.scrape_type == 'ALL' else int(self.scrape_type)

    def get_max_page_num(self):
        soup = self.create_soup(self.base_url.format(pg_num='1'))
        max_pg = int(soup.find('ul',{'class':'pt-cv-pagination pt-cv-ajax pagination'}).get('data-totalpages'))
        return max_pg

    @task_timer
    def scrape_page(self, pg_num):
        soup = self.create_soup(self.base_url.format(pg_num=str(pg_num)))
        recipes = []
        for article in soup.find_all('div', {'class':'col-md-4 col-sm-4 col-xs-6 pt-cv-content-item pt-cv-1-col'}):
            link = article.find('a')['href']
            title = article.find('h4').text
            image = article.find('img')['src']
            recipes.append(('Delightful Plate', title, link, image))
        return recipes

    def scrape_all_pages(self):
        recipes = []

        for pg_num in range(1, self.max_pg + 1):
            logger.info(f"Scraping page number: {str(pg_num)}")
            recipes.extend(self.scrape_page(pg_num))
            # wait for a while
            time.sleep(3)
        return recipes

