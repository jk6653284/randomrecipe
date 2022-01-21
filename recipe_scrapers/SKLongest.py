import os
import re
import sys
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger

class SKLongest(RecipeScraper):
    def __init__(self):
        super(SKLongest, self).__init__()
        self.base_url = "https://seonkyounglongest.com/recipe/page/{pg_num}/"
        self.max_pg = self.get_max_page_num() if self.scrape_type == 'ALL' else int(self.scrape_type)

    def get_max_page_num(self):
        soup = self.create_soup(self.base_url.format(pg_num=str(1)))
        max_pg = int(soup.find_all('a',{'class':'page-numbers'})[-2].text)
        return max_pg

    @task_timer
    def scrape_page(self, pg_num):
        soup = self.create_soup(self.base_url.format(pg_num=str(pg_num)))
        recipes = []
        for article in soup.find_all('article'):
            title = article.find('h2').text
            link = article.find('h2').find('a')['href']
            try:
                image = article.find('a',{'class':'penci-image-holder'})['style'].split("('")[-1].split("')")[0]
            except BaseException:
                logger.info(f"No image available for {title}.")
                image = ""
            recipes.append(('SeonKyoung', title, link, image))
        return recipes

    def scrape_all_pages(self):
        recipes = []
        for pg_num in range(1, self.max_pg+1):
            logger.info(f"Scraping page number: {str(pg_num)}")
            recipes.extend(self.scrape_page(str(pg_num)))
            # wait for a while
            time.sleep(3)
        return recipes