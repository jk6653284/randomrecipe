# imports
import sys

# import scrapers
from BudgetBytes import BudgetBytes
from Food52 import Food52
from IAmaFB import IAmaFB
from JustOneCB import JustOneCB
from KitchenStories import KitchenStories
from SeriousEats import SeriousEats
from Ottolenghi import Ottolenghi
from WoksOfLife import WoksOfLife
from HalfBakedHarvest import HalfBakedHarvest
from SweetPillarFood import SweetPillarFood
from DelightfulPlate import DelightfulPlate
from Lacucina import Lacucina
from JapCook101 import JapCook101
from SKLongest import SKLongest
from SpoonForkBacon import SpoonForkBacon

def run_scraper(scraper):
    recipes = scraper.scrape_all_pages()
    # only insert to table if length is more than 0
    if len(recipes) > 0:
        scraper.export_data(recipes)

def main():
    run_scraper(BudgetBytes())
    run_scraper(Food52())
    run_scraper(JustOneCB())
    run_scraper(KitchenStories())
    run_scraper(SeriousEats())
    run_scraper(IAmaFB())
    run_scraper(Ottolenghi())
    run_scraper(WoksOfLife())
    run_scraper(HalfBakedHarvest())
    run_scraper(SweetPillarFood())
    run_scraper(DelightfulPlate())
    run_scraper(Lacucina())
    run_scraper(JapCook101())
    run_scraper(SKLongest())
    run_scraper(SpoonForkBacon())


if __name__ == '__main__':
    main()
