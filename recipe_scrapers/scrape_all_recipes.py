# imports
import sys

# import scrapers
from BudgetBytes import BudgetBytes
from Food52 import Food52
from IAmaFB import IAmaFB
from JustOneCB import JustOneCB
from KitchenStories import KitchenStories
from SeriousEats import SeriousEats

# import logger
sys.path.append("../")
from logger import logger

def run_scraper(scraper):
    recipes = scraper.scrape_all_pages()
    scraper.export_data(recipes)


def main():
    run_scraper(BudgetBytes())
    run_scraper(Food52())
    #run_scraper(IAmaFB())
    run_scraper(JustOneCB())
    run_scraper(KitchenStories())
    run_scraper(SeriousEats())


if __name__ == '__main__':
    main()
