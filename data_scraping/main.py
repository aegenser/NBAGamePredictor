import playerScraper
import gameScraper
import seasonScraper
# import datetime
import pickle
import numpy as np

def main():
    # print(playerScraper.scrapePlayer("bolbo01"))
    # print(playerScraper.scrapePlayer("smartma01"))
    # print(playerScraper.scrapePlayer("onealsh01"))
    # game = gameScraper.scrapeGame("2002", "01", "12", "CHI")
    # print(game.result)
    # print(len(game.away_starters))
    # print(len(game.away_bench))
    # print(len(game.home_starters))
    # print(len(game.home_bench))
    # print(game.away_bench[0].tag)
    # print(game.home_bench[0].tag)
    # date1 = datetime.date(2020, 7, 25)
    # date2 = datetime.date(2020, 7, 20)
    # print((date1-date2).days)
    try:
        with open('players.dictionary', 'rb') as f:
            players = pickle.load(f)
    except:
        players = {}

    data = []
    # season_settings = [ \
    #                     [2000, 10, 31, 2001, 6, 15, '01'], \
    #                     [2001, 10, 30, 2002, 6, 12, '02'], \
    #                     [2002, 10, 29, 2003, 6, 15, '03'], \
    #                     [2003, 10, 28, 2004, 6, 15, '04'], \
    #                     [2004, 11, 2, 2005, 6, 23, '05'], \
    #                     [2005, 11, 1, 2006, 6, 20, '06'], \
    #                     [2006, 10, 31, 2007, 6, 14, '07'], \
    #                     [2007, 10, 30, 2008, 6, 17, '08'], \
    #                     [2008, 10, 28, 2009, 6, 14, '09'], \
    #                     [2009, 10, 27, 2010, 6, 17, '10'], \
    #                     [2010, 10, 26, 2011, 6, 12, '11'], \
    #                     [2011, 12, 25, 2012, 6, 21, '12'], \
    #                     [2012, 10, 30, 2013, 6, 20, '13'], \
    #                     [2013, 10, 29, 2014, 6, 15, '14'], \
    #                     [2014, 10, 28, 2015, 6, 16, '15'], \
    #                     [2015, 10, 27, 2016, 6, 19, '16'], \
    #                     [2016, 10, 25, 2017, 6, 12, '17'], \
    #                     [2017, 10, 17, 2018, 6, 8, '18'], \
    #                     [2018, 10, 16, 2019, 6, 13, '19'], \
    #                     [2019, 10, 22, 2020, 3, 11, '20'], \
    #                   ]

    for ss in ['05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']:
        seasonScraper.scrapeSeasonV2(players, ss, data)
        np.savetxt('data.csv', data, delimiter=',')
        with open('players.dictionary', 'wb') as f:
            pickle.dump(players, f)
        

if __name__ == '__main__':
    main()