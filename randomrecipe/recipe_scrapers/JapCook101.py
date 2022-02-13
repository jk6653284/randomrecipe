import os
import sys
import time

from _scrape_data import task_timer, RecipeScraper

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

class JapCook101(RecipeScraper):
    def __init__(self):
        super(JapCook101, self).__init__()
        self.base_url = "https://www.japanesecooking101.com/page/{pg_num}/?s"

    @task_timer
    def scrape_page(self, pg_num):
        soup = self.create_soup(self.base_url.format(pg_num=str(pg_num)),
                                headers=headers)
        recipes = []
        articles = soup.find_all('article')
        if len(articles) == 0:
            return False
        else:
            for article in articles:
                link = article.find('h2').find('a')['href']
                title = article.find('h2').find('a').text
                recipes.append(('Japanese Cooking 101', title, link))
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