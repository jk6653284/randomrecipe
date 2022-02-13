import os
import re
import sys
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger


class IAmaFB(RecipeScraper):
    def __init__(self):
        super(IAmaFB, self).__init__()
        self.base_url = "https://iamafoodblog.com/category/recipes/page"

    @task_timer
    def scrape_page(self, pg_num):
        soup = self.create_soup(f"{self.base_url}/{str(pg_num)}/")
        recipes = []
        articles = soup.findAll("div", {"class": re.compile(r'archive-tile archive-[\d+]')})
        if len(articles) == 0:
            return False
        else:
            for article in articles:
                link = article.find('a')['href']
                title = article.find('h2').text
                recipes.append(('I Am a Food Blog', title, link))
        return recipes

    def scrape_all_pages(self):
        recipes = []
        if self.scrape_type == 'ALL':
            pg_num = 1
            while True:
                result = self.scrape_page(str(pg_num))
                if not result:
                    break
                else:
                    logger.info(f"Scraping page number: {str(pg_num)}")
                    recipes.extend(result)
                    pg_num += 1
                time.sleep(3)
        else:
            for pg_num in range(1, int(self.scrape_type) + 1):
                logger.info(f"Scraping page number: {str(pg_num)}")
                result = self.scrape_page(str(pg_num))
                recipes.extend(result)
                time.sleep(3)
        return recipes
