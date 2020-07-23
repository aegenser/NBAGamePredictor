import playerScraper
import gameScraper

def main():
    # print(playerScraper.scrapePlayer("harrito02"))
    # print(playerScraper.scrapePlayer("smartma01"))
    # print(playerScraper.scrapePlayer("rosede01"))
    gameScraper.scrapeGame("2019", "02", "26", "TOR")

if __name__ == '__main__':
    main()