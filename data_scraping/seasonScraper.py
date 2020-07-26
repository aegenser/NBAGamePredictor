from bs4 import BeautifulSoup as bsoup
import urllib.request
import constant
import gameScraper
import playerScraper
import datetime
import time

def initialize_player():
    player = {}
    player['g'] = 0
    player['gs'] = 0
    player['mp'] = 0
    player['orb'] = 0
    player['drb'] = 0
    player['ast'] = 0
    player['blk'] = 0
    player['stl'] = 0
    player['tov'] = 0
    player['pf'] = 0
    player['fta'] = 0
    player['ftm'] = 0
    player['fg3a'] = 0
    player['fg3m'] = 0
    player['fg2a'] = 0
    player['fg2m'] = 0
    return player

def safe_divide(a, b):
    if b == 0:
        return 0
    else:
        return a / b

def processGame(game, players, players_this_season, players_this_postseason, teams, season, data):
    new_row = []
    # Game: 
    # - is playoff game
    # Teams:
    # - % of games won so far
    # - % of games won at home
    # - % of games at home
    # - % of games with this starting 5
    # - win % w/ this starting 5
    # - days since last game (max 7)
    # Players:
    # - stuff
    if game.is_playoff_game:
        new_row.append(1.0)
    else:
        new_row.append(0.0)

    home_starting = []
    for stat_line in game.home_starters:
        home_starting.append(stat_line.tag)
    home_starting.sort()
    home_starting_str = ""
    for tag in home_starting:
        home_starting_str += tag

    away_starting = []
    for stat_line in game.away_starters:
        away_starting.append(stat_line.tag)
    away_starting.sort()
    away_starting_str = ""
    for tag in away_starting:
        away_starting_str += tag
    
    if game.home_team not in teams:
        new_row += [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    else:
        new_row.append(round(teams[game.home_team]['games_played'] / constant.G_SCLR, 3))
        new_row.append(round(teams[game.home_team]['games_won'] / teams[game.home_team]['games_played'], 3))
        new_row.append(round(safe_divide(teams[game.home_team]['games_won_home'], teams[game.home_team]['games_played_home']), 3))
        new_row.append(round(teams[game.home_team]['games_played_home'] / teams[game.home_team]['games_played'], 3))
        if (home_starting_str + '_played') in teams[game.home_team]:
            new_row.append(round(teams[game.home_team][home_starting_str + '_played'] / teams[game.home_team]['games_played'], 3))
            new_row.append(round(teams[game.home_team][home_starting_str + '_won'] / teams[game.home_team][home_starting_str + '_played'], 3))
        else:
            new_row += [0.0, 0.0]

        new_row.append(min(1.0, round((game.date - teams[game.home_team]['last_game']).days / 7, 3)))

    if game.away_team not in teams:
        new_row += [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    else:
        new_row.append(round(teams[game.away_team]['games_played'] / constant.G_SCLR, 3))
        new_row.append(round(teams[game.away_team]['games_won'] / teams[game.away_team]['games_played'], 3))
        new_row.append(round(safe_divide(teams[game.away_team]['games_won_home'], teams[game.away_team]['games_played_home']), 3))
        new_row.append(round(teams[game.away_team]['games_played_home'] / teams[game.away_team]['games_played'], 3))
        if (away_starting_str + '_played') in teams[game.away_team]:
            new_row.append(round(teams[game.away_team][away_starting_str + '_played'] / teams[game.away_team]['games_played'], 3))
            new_row.append(round(teams[game.away_team][away_starting_str + '_won'] / teams[game.away_team][away_starting_str + '_played'], 3))
        else:
            new_row += [0.0, 0.0]

        new_row.append(min(1.0, round((game.date - teams[game.away_team]['last_game']).days / 7, 3)))

    home = True
    player_tags = home_starting + list(map(lambda player: player.tag, game.home_bench))
    player_tags.append('switch')
    player_tags += away_starting + list(map(lambda player: player.tag, game.away_bench))

    for player in player_tags:
        player_data = []
        if player == 'switch':
            for _ in range((8 - len(game.home_bench))*168):
                new_row.append(0.0)
            home = False
            continue
        if player not in players:
            time.sleep(.5)
            players[player] = playerScraper.scrapePlayer(player)

        player_data.append(round((players[player]['height'] - constant.HEIGHT_MIN) / constant.HEIGHT_SCLR, 3))
        player_data.append(round((players[player]['weight'] - constant.WEIGHT_MIN) / constant.WEIGHT_SCLR, 3))
        player_age = (game.date - players[player]['birthday']).days
        player_data.append(round((player_age - constant.AGE_MIN) / constant.AGE_SCLR, 3))

        season_year = int(season) + 2000
        for year in range(season_year-3, season_year):
            if (str(year)[-2:]) in players[player]:
                player_data += players[player][str(year)[-2:]]
            else:
                player_data += [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        for year in range(season_year-3, season_year):
            if ('playoff' + str(year)[-2:]) in players[player]:
                player_data += players[player]['playoff' + str(year)[-2:]]
            else:
                player_data += [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        if player not in players_this_season:
            players_this_season[player] = initialize_player()

        player_data.append(round((players_this_season[player]['g'] / constant.G_SCLR), 3))
        player_data.append(round((players_this_season[player]['gs'] / constant.G_SCLR), 3))
        player_data.append(round(safe_divide(players_this_season[player]['mp'], players_this_season[player]['g']) / constant.MP_SCLR, 3))
        player_data.append(round(safe_divide(players_this_season[player]['orb'], players_this_season[player]['g']) / constant.ORB_SCLR, 3))
        player_data.append(round(safe_divide(players_this_season[player]['drb'], players_this_season[player]['g']) / constant.DRB_SCLR, 3))
        player_data.append(round(safe_divide(players_this_season[player]['ast'], players_this_season[player]['g']) / constant.AST_SCLR, 3))
        player_data.append(round(safe_divide(players_this_season[player]['blk'], players_this_season[player]['g']) / constant.BLK_SCLR, 3))
        player_data.append(round(safe_divide(players_this_season[player]['stl'], players_this_season[player]['g']) / constant.STL_SCLR, 3))
        player_data.append(round(safe_divide(players_this_season[player]['tov'], players_this_season[player]['g']) / constant.TOV_SCLR, 3))
        player_data.append(round(safe_divide(players_this_season[player]['pf'], players_this_season[player]['g']) / constant.PF_SCLR, 3))
        player_data.append(round(safe_divide(players_this_season[player]['fta'], players_this_season[player]['g']) / constant.FTA_SCLR, 3))
        player_data.append(round(safe_divide(players_this_season[player]['ftm'], players_this_season[player]['fta']), 3))
        player_data.append(round(safe_divide(players_this_season[player]['fg3a'], players_this_season[player]['g']) / constant.FG3A_SCLR, 3))
        player_data.append(round(safe_divide(players_this_season[player]['fg3m'], players_this_season[player]['fg3a']), 3))
        player_data.append(round(safe_divide(players_this_season[player]['fg2a'], players_this_season[player]['g']) / constant.FG2A_SCLR, 3))
        player_data.append(round(safe_divide(players_this_season[player]['fg2m'], players_this_season[player]['fg2a']), 3))

        if player not in players_this_postseason:
            players_this_postseason[player] = initialize_player()

        player_data.append(round((players_this_postseason[player]['g'] / constant.G_SCLR), 3))
        player_data.append(round((players_this_postseason[player]['gs'] / constant.G_SCLR), 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['mp'], players_this_postseason[player]['g']) / constant.MP_SCLR, 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['orb'], players_this_postseason[player]['g']) / constant.ORB_SCLR, 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['drb'], players_this_postseason[player]['g']) / constant.DRB_SCLR, 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['ast'], players_this_postseason[player]['g']) / constant.AST_SCLR, 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['blk'], players_this_postseason[player]['g']) / constant.BLK_SCLR, 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['stl'], players_this_postseason[player]['g']) / constant.STL_SCLR, 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['tov'], players_this_postseason[player]['g']) / constant.TOV_SCLR, 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['pf'], players_this_postseason[player]['g']) / constant.PF_SCLR, 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['fta'], players_this_postseason[player]['g']) / constant.FTA_SCLR, 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['ftm'], players_this_postseason[player]['fta']), 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['fg3a'], players_this_postseason[player]['g']) / constant.FG3A_SCLR, 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['fg3m'], players_this_postseason[player]['fg3a']), 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['fg2a'], players_this_postseason[player]['g']) / constant.FG2A_SCLR, 3))
        player_data.append(round(safe_divide(players_this_postseason[player]['fg2m'], players_this_postseason[player]['fg2a']), 3))

        if home:
            if game.home_team not in players_this_season[player]:
                players_this_season[player][game.home_team] = 0
            player_data.append(round(safe_divide(players_this_season[player][game.home_team], players_this_season[player]['g'] + players_this_postseason[player]['g']), 3))
        else:
            if game.away_team not in players_this_season[player]:
                players_this_season[player][game.away_team] = 0
            player_data.append(round(safe_divide(players_this_season[player][game.away_team], players_this_season[player]['g'] + players_this_postseason[player]['g']), 3))

        if len(player_data) != 168:
            print('Error: player data wrong length')
            raise
        new_row += player_data 

    for _ in range((8 - len(game.away_bench))*168):
        new_row.append(0.0)
    new_row.append(game.result)
    # create data entry
    if data != []:
        if len(data[0]) != len(new_row):
            print(game.date)
            print(game.home_team)
            print(len(data[0]))
            print(len(new_row))
            raise
    data.append(new_row)
    # update player totals (games with team, games, all stat totals)
    if game.home_team not in teams:
        teams[game.home_team] = {}
        teams[game.home_team]['games_played'] = 0
        teams[game.home_team]['games_won'] = 0
        teams[game.home_team]['games_played_home'] = 0
        teams[game.home_team]['games_won_home'] = 0

    if game.away_team not in teams:
        teams[game.away_team] = {}
        teams[game.away_team]['games_played'] = 0
        teams[game.away_team]['games_won'] = 0
        teams[game.away_team]['games_played_home'] = 0
        teams[game.away_team]['games_won_home'] = 0

    if (away_starting_str + '_played') not in teams[game.away_team]:
        teams[game.away_team][away_starting_str + '_played'] = 0
        teams[game.away_team][away_starting_str + '_won'] = 0

    if (home_starting_str + '_played') not in teams[game.home_team]:
        teams[game.home_team][home_starting_str + '_played'] = 0
        teams[game.home_team][home_starting_str + '_won'] = 0

    teams[game.home_team]['games_played'] += 1
    teams[game.home_team][home_starting_str + '_played'] += 1
    teams[game.away_team]['games_played'] += 1
    teams[game.away_team][away_starting_str + '_played'] += 1
    teams[game.home_team]['games_played_home'] += 1
    if game.result > 0:
         teams[game.home_team]['games_won'] += 1
         teams[game.home_team]['games_won_home'] += 1
         teams[game.home_team][home_starting_str + '_won'] += 1
    else:
        teams[game.away_team]['games_won'] += 1
        teams[game.away_team][away_starting_str + '_won'] += 1

    teams[game.home_team]['last_game'] = game.date
    teams[game.away_team]['last_game'] = game.date

    for stat_line in game.home_starters + game.away_starters:
        if game.is_playoff_game:
            players_this_postseason[stat_line.tag]['gs'] += 1
        else:
            players_this_season[stat_line.tag]['gs'] += 1

    for stat_line in game.home_starters + game.home_bench:
        if game.home_team in players_this_season[stat_line.tag]:
            players_this_season[stat_line.tag][game.home_team] += 1
        else:
            players_this_season[stat_line.tag][game.home_team] = 1

    for stat_line in game.away_starters + game.away_bench:
        if game.away_team in players_this_season[stat_line.tag]:
            players_this_season[stat_line.tag][game.away_team] += 1
        else:
            players_this_season[stat_line.tag][game.away_team] = 1

    for stat_line in game.home_starters + game.home_bench + game.away_starters + game.away_bench:
        if game.is_playoff_game:
            players_this_postseason[stat_line.tag]['g'] += 1
            players_this_postseason[stat_line.tag]['mp'] += stat_line.min
            players_this_postseason[stat_line.tag]['orb'] += stat_line.orb
            players_this_postseason[stat_line.tag]['drb'] += stat_line.drb
            players_this_postseason[stat_line.tag]['ast'] += stat_line.ast
            players_this_postseason[stat_line.tag]['blk'] += stat_line.blk
            players_this_postseason[stat_line.tag]['stl'] += stat_line.stl
            players_this_postseason[stat_line.tag]['tov'] += stat_line.tov
            players_this_postseason[stat_line.tag]['pf'] += stat_line.pf
            players_this_postseason[stat_line.tag]['fta'] += stat_line.fta
            players_this_postseason[stat_line.tag]['ftm'] += stat_line.ft
            players_this_postseason[stat_line.tag]['fg3a'] += stat_line.three_pt_attempts
            players_this_postseason[stat_line.tag]['fg3m'] += stat_line.three_pt_made
            players_this_postseason[stat_line.tag]['fg2a'] += stat_line.two_pt_attempts
            players_this_postseason[stat_line.tag]['fg2m'] += stat_line.two_pt_attempts
        else:
            players_this_season[stat_line.tag]['g'] += 1
            players_this_season[stat_line.tag]['mp'] += stat_line.min
            players_this_season[stat_line.tag]['orb'] += stat_line.orb
            players_this_season[stat_line.tag]['drb'] += stat_line.drb
            players_this_season[stat_line.tag]['ast'] += stat_line.ast
            players_this_season[stat_line.tag]['blk'] += stat_line.blk
            players_this_season[stat_line.tag]['stl'] += stat_line.stl
            players_this_season[stat_line.tag]['tov'] += stat_line.tov
            players_this_season[stat_line.tag]['pf'] += stat_line.pf
            players_this_season[stat_line.tag]['fta'] += stat_line.fta
            players_this_season[stat_line.tag]['ftm'] += stat_line.ft
            players_this_season[stat_line.tag]['fg3a'] += stat_line.three_pt_attempts
            players_this_season[stat_line.tag]['fg3m'] += stat_line.three_pt_made
            players_this_season[stat_line.tag]['fg2a'] += stat_line.two_pt_attempts
            players_this_season[stat_line.tag]['fg2m'] += stat_line.two_pt_attempts

def scrapeSeason(start_year, start_month, start_day, end_year, end_month, end_day, players, season, data):
    players_this_season = {}
    players_this_postseason = {}
    teams = {}

    year = start_year
    month = start_month
    day = start_day
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

        print(strYear+strMonth+strDay)
        for team in constant.TEAMS:
            game = gameScraper.scrapeGame(strYear, strMonth, strDay, team)
            time.sleep(1)
            if game != None:
                processGame(game, players, players_this_season, players_this_postseason, teams, season, data)
        if day == 31:
            day = 1
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
        else:
            day += 1

        if month == end_month and day == end_day and year == end_year:
            with open(season + 'players.dictionary', 'wb') as f:
                pickle.dump(players_this_season, f)
            with open(season + 'players_playoffs.dictionary', 'wb') as f:
                pickle.dump(players_this_postseason, f)
            with open(season + 'teams.dictionary', 'wb') as f:
                pickle.dump(teams, f)
            break

    

    
