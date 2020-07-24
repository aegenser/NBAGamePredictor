from bs4 import BeautifulSoup as bsoup
import urllib.request
import constant
import gameScraper

def processGame(game, players, players_this_season, data):
    new_row = []
    # create data entry
    data.append(new_row)
    # update player totals (games with team, games, all stat totals)

def scrapeSeason(year, start_year, start_month, end_year, end_month, players, data):
    players_this_season = {}

    year = start_year
    month = start_month
    day = 1
    while(True):
        strYear = str(year)
        if month < 10:
            strMonth = "0" + str(month)
        else:
            strMonth = str(month)
        if day < 10:
            strDay = "0" + str(day)
        else:
            strDay = str(day)
        for team in constant.TEAMS:
            game = scrapeGame(strYear, strMonth, strDay, team)
            time.sleep(2)
            if game != None:
                processGame(game, players, players_this_season, data)
        if day == 31:
            day = 1
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
        else:
            day += 1

        if month == end_month and day == 31 and year == end_month:
            break

    
