import xgboost as xgb
import copy
import random
import datetime
import numpy as np
import constant

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

class Simulation:
    def __init__(self, teams, players, players_this_season, players_this_postseason, schedule, model, lineups, matchups, results):
        self.teams = copy.deepcopy(teams)
        self.players = players
        self.players_this_season = players_this_season
        self.model = model
        self.lineups = lineups
        self.schedule = schedule
        self.players_this_postseason = players_this_postseason
        self.matchups = matchups
        self.results = results

    # simulates team1 winning a game over team 2
    def simulate_win(self, team1, team2, date, is_playoff_game, team1_win):
        home_starting_str = ""
        for tag in sorted(self.lineups[team1]):
            home_starting_str += tag

        away_starting_str = ""
        for tag in sorted(self.lineups[team2]):
            away_starting_str += tag

        if (away_starting_str + '_played') not in self.teams[team2]:
            self.teams[team2][away_starting_str + '_played'] = 0
            self.teams[team2][away_starting_str + '_won'] = 0

        if (home_starting_str + '_played') not in self.teams[team1]:
            self.teams[team1][home_starting_str + '_played'] = 0
            self.teams[team1][home_starting_str + '_won'] = 0

        self.teams[team1]['games_played'] += 1
        self.teams[team1][home_starting_str + '_played'] += 1
        self.teams[team2]['games_played'] += 1
        self.teams[team2][away_starting_str + '_played'] += 1
        self.teams[team1]['games_played_home'] += 1
        if team1_win:
            self.teams[team1]['games_won'] += 1
            self.teams[team1]['games_won_home'] += 1
            self.teams[team1][home_starting_str + '_won'] += 1
        else:
            self.teams[team2]['games_won'] += 1
            self.teams[team2][away_starting_str + '_won'] += 1

        self.teams[team1]['last_game'] = date
        self.teams[team2]['last_game'] = date

    # returns True if team1 wins
    def simulate_game(self, team1, team2, date, is_playoff_game):
        new_row = []
        if is_playoff_game:
            new_row.append(1.0)
        else:
            new_row.append(0.0)

        home_starting_str = ""
        for tag in sorted(self.lineups[team1]):
            home_starting_str += tag

        away_starting_str = ""
        for tag in sorted(self.lineups[team2]):
            away_starting_str += tag

        new_row.append(round(self.teams[team1]['games_played'] / constant.G_SCLR, 3))
        new_row.append(round(self.teams[team1]['games_won'] / self.teams[team1]['games_played'], 3))
        new_row.append(round(safe_divide(self.teams[team1]['games_won_home'], self.teams[team1]['games_played_home']), 3))
        new_row.append(round(self.teams[team1]['games_played_home'] / self.teams[team1]['games_played'], 3))
        if (home_starting_str + '_played') in self.teams[team1]:
            new_row.append(round(self.teams[team1][home_starting_str + '_played'] / self.teams[team1]['games_played'], 3))
            new_row.append(round(self.teams[team1][home_starting_str + '_won'] / self.teams[team1][home_starting_str + '_played'], 3))
        else:
            new_row += [0.0, 0.0]

        new_row.append(min(1.0, round((date - self.teams[team1]['last_game']).days / 7, 3)))

        new_row.append(round(self.teams[team2]['games_played'] / constant.G_SCLR, 3))
        new_row.append(round(self.teams[team2]['games_won'] / self.teams[team2]['games_played'], 3))
        new_row.append(round(safe_divide(self.teams[team2]['games_won_home'], self.teams[team2]['games_played_home']), 3))
        new_row.append(round(self.teams[team2]['games_played_home'] / self.teams[team2]['games_played'], 3))
        if (home_starting_str + '_played') in self.teams[team2]:
            new_row.append(round(self.teams[team2][home_starting_str + '_played'] / self.teams[team2]['games_played'], 3))
            new_row.append(round(self.teams[team2][home_starting_str + '_won'] / self.teams[team2][home_starting_str + '_played'], 3))
        else:
            new_row += [0.0, 0.0]

        new_row.append(min(1.0, round((date - self.teams[team2]['last_game']).days / 7, 3)))

        player_tags = self.lineups[team1] + ['switch'] + self.lineups[team2]
        home = True
        for player in player_tags:
            player_data = []
            if player == 'switch':
                for _ in range((13 - len(self.lineups[team1]))*168):
                    new_row.append(0.0)
                home = False
                continue

            player_data.append(round((self.players[player]['height'] - constant.HEIGHT_MIN) / constant.HEIGHT_SCLR, 3))
            player_data.append(round((self.players[player]['weight'] - constant.WEIGHT_MIN) / constant.WEIGHT_SCLR, 3))
            player_age = (date - self.players[player]['birthday']).days
            player_data.append(round((player_age - constant.AGE_MIN) / constant.AGE_SCLR, 3))

            season_year = 2020
            for year in range(season_year-3, season_year):
                if (str(year)[-2:]) in self.players[player]:
                    player_data += self.players[player][str(year)[-2:]]
                else:
                    player_data += [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            for year in range(season_year-3, season_year):
                if ('playoff' + str(year)[-2:]) in self.players[player]:
                    player_data += self.players[player]['playoff' + str(year)[-2:]]
                else:
                    player_data += [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            if player not in self.players_this_season:
                self.players_this_season[player] = initialize_player()

            if player not in self.players_this_postseason:
                self.players_this_postseason[player] = initialize_player()

            player_data.append(round((self.players_this_season[player]['g'] / constant.G_SCLR), 3))
            player_data.append(round((self.players_this_season[player]['gs'] / constant.G_SCLR), 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['mp'], self.players_this_season[player]['g']) / constant.MP_SCLR, 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['orb'], self.players_this_season[player]['g']) / constant.ORB_SCLR, 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['drb'], self.players_this_season[player]['g']) / constant.DRB_SCLR, 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['ast'], self.players_this_season[player]['g']) / constant.AST_SCLR, 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['blk'], self.players_this_season[player]['g']) / constant.BLK_SCLR, 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['stl'], self.players_this_season[player]['g']) / constant.STL_SCLR, 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['tov'], self.players_this_season[player]['g']) / constant.TOV_SCLR, 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['pf'], self.players_this_season[player]['g']) / constant.PF_SCLR, 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['fta'], self.players_this_season[player]['g']) / constant.FTA_SCLR, 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['ftm'], self.players_this_season[player]['fta']), 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['fg3a'], self.players_this_season[player]['g']) / constant.FG3A_SCLR, 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['fg3m'], self.players_this_season[player]['fg3a']), 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['fg2a'], self.players_this_season[player]['g']) / constant.FG2A_SCLR, 3))
            player_data.append(round(safe_divide(self.players_this_season[player]['fg2m'], self.players_this_season[player]['fg2a']), 3))

            player_data += [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            if home:
                if team1 not in self.players_this_season[player]:
                    self.players_this_season[player][team1] = 0
                player_data.append(round(safe_divide(self.players_this_season[player][team1], self.players_this_season[player]['g'] + self.players_this_postseason[player]['g']), 3))
            else:
                if team2 not in self.players_this_season[player]:
                    self.players_this_season[player][team2] = 0
                player_data.append(round(safe_divide(self.players_this_season[player][team2], self.players_this_season[player]['g'] + self.players_this_postseason[player]['g']), 3))

            if len(player_data) != 168:
                print('Error: player data wrong length')
                raise
            new_row += player_data

        for _ in range((13 - len(self.lineups[team2]))*168):
            new_row.append(0.0)

        new_row = np.array([new_row])
        prediction = self.model.predict(xgb.DMatrix(new_row))[0]
        newer_row = np.zeros(new_row.shape)
        newer_row[:, 1:8] = new_row[:, 8:15]
        newer_row[:, 8:15] = new_row[:, 1:8]
        newer_row[:, 15:2199] = new_row[:, 2199:]
        newer_row[:, 2199:] = new_row[:, 15:2199]
        prediction = (1-self.model.predict(xgb.DMatrix(newer_row))[0]+prediction) / 2
        prediction = prediction > random.random()

        if (away_starting_str + '_played') not in self.teams[team2]:
            self.teams[team2][away_starting_str + '_played'] = 0
            self.teams[team2][away_starting_str + '_won'] = 0

        if (home_starting_str + '_played') not in self.teams[team1]:
            self.teams[team1][home_starting_str + '_played'] = 0
            self.teams[team1][home_starting_str + '_won'] = 0

        self.teams[team1]['games_played'] += 1
        self.teams[team1][home_starting_str + '_played'] += 1
        self.teams[team2]['games_played'] += 1
        self.teams[team2][away_starting_str + '_played'] += 1
        self.teams[team1]['games_played_home'] += 1
        if prediction:
            self.teams[team1]['games_won'] += 1
            self.teams[team1]['games_won_home'] += 1
            self.teams[team1][home_starting_str + '_won'] += 1
        else:
            self.teams[team2]['games_won'] += 1
            self.teams[team2][away_starting_str + '_won'] += 1

        self.teams[team1]['last_game'] = date
        self.teams[team2]['last_game'] = date

        return prediction

    def simulate_series(self, team1, team2, start_date):
        if tuple(sorted([team1, team2])) not in self.matchups:
            self.matchups[tuple(sorted([team1, team2]))] = 0
        self.matchups[tuple(sorted([team1, team2]))] += 1

        team1_wins = 0
        team2_wins = 0
        date = copy.copy(start_date)
        while(team1_wins < 4 and team2_wins < 4):
            if self.simulate_game(team1, team2, date, True):
                team1_wins += 1
            else:
                team2_wins += 1
            date = date + datetime.timedelta(3)

        if team1_wins == 4:
            return date, team1
        return date, team2

    def simulate_playin(self, team1, team2, start_date):
        team1_wins = 1
        team2_wins = 0

        date = copy.copy(start_date)
        while(team1_wins < 2 and team2_wins < 2):
            if self.simulate_game(team1, team2, date, True):
                team1_wins += 1
            else:
                team2_wins += 1
            date = date + datetime.timedelta(2)

        if team1_wins == 2:
            return date, team1
        return date, team2

    def simulate_reg_season(self):
        for game in self.schedule:
            if 'result' in game:
                self.simulate_win(game['team1'], game['team2'], game['date'], False, game['result'])
            else: 
                self.simulate_game(game['team1'], game['team2'], game['date'], False)

    def simulate_playoffs(self, start_date):
        western_conference = ['LAL', 'LAC', 'DEN', 'UTA', 'OKC', 'HOU', 'DAL', 'MEM', 'POR', 'NOP', 'SAC', 'PHO', 'SAS']
        eastern_conference = ['MIL', 'TOR', 'BOS', 'MIA', 'IND', 'PHI', 'BRK', 'ORL', 'WAS']
        western_conference.sort(key=lambda team : self.teams[team]['games_won'] / self.teams[team]['games_played'], reverse = True)
        eastern_conference.sort(key=lambda team : self.teams[team]['games_won'] / self.teams[team]['games_played'], reverse = True)

        west_gb = 2 * self.teams[western_conference[7]]['games_won'] - self.teams[western_conference[7]]['games_played'] \
                  - (2 * self.teams[western_conference[8]]['games_won'] - self.teams[western_conference[8]]['games_played'])

        west_date = copy.copy(start_date)
        if west_gb <= 4:
            west_date, western_conference[7] = self.simulate_playin(western_conference[7], western_conference[8], west_date)

        east_gb = 2 * self.teams[eastern_conference[7]]['games_won'] - self.teams[eastern_conference[7]]['games_played'] \
                  - (2 * self.teams[eastern_conference[8]]['games_won'] - self.teams[eastern_conference[8]]['games_played'])

        east_date = copy.copy(start_date)
        if east_gb <= 4:
            east_date, eastern_conference[7] = self.simulate_playin(eastern_conference[7], eastern_conference[8], east_date)

        for team in western_conference[:8] + eastern_conference[:8]:
            if team not in self.results['playoffs']:
                self.results['playoffs'][team] = 0
            self.results['playoffs'][team] += 1

        west_8_1_date, west_8_1_winner = self.simulate_series(western_conference[0], western_conference[7], west_date)
        west_7_2_date, west_7_2_winner = self.simulate_series(western_conference[1], western_conference[6], west_date)
        west_6_3_date, west_6_3_winner = self.simulate_series(western_conference[2], western_conference[5], west_date)
        west_5_4_date, west_5_4_winner = self.simulate_series(western_conference[3], western_conference[4], west_date)
        east_8_1_date, east_8_1_winner = self.simulate_series(eastern_conference[0], eastern_conference[7], east_date)
        east_7_2_date, east_7_2_winner = self.simulate_series(eastern_conference[1], eastern_conference[6], east_date)
        east_6_3_date, east_6_3_winner = self.simulate_series(eastern_conference[2], eastern_conference[5], east_date)
        east_5_4_date, east_5_4_winner = self.simulate_series(eastern_conference[3], eastern_conference[4], east_date)

        for team in [west_8_1_winner, west_7_2_winner, west_6_3_winner, west_5_4_winner, east_8_1_winner, east_7_2_winner, east_6_3_winner, east_5_4_winner]:
            if team not in self.results['semi']:
                self.results['semi'][team] = 0
            self.results['semi'][team] += 1

        west_semi1_date, west_semi1_winner = self.simulate_series(west_8_1_winner, west_5_4_winner, max(west_8_1_date, west_5_4_date))
        west_semi2_date, west_semi2_winner = self.simulate_series(west_7_2_winner, west_6_3_winner, max(west_7_2_date, west_6_3_date))
        east_semi1_date, east_semi1_winner = self.simulate_series(east_8_1_winner, east_5_4_winner, max(east_8_1_date, east_5_4_date))
        east_semi2_date, east_semi2_winner = self.simulate_series(east_7_2_winner, east_6_3_winner, max(east_7_2_date, east_6_3_date))

        for team in [west_semi1_winner, west_semi2_winner, east_semi1_winner, east_semi2_winner]:
            if team not in self.results['conf']:
                self.results['conf'][team] = 0
            self.results['conf'][team] += 1

        west_date, west_winner = self.simulate_series(west_semi2_winner, west_semi1_winner, max(west_semi1_date, west_semi2_date))
        east_date, east_winner = self.simulate_series(east_semi1_winner, east_semi2_winner, max(east_semi1_date, east_semi2_date))

        for team in [west_winner, east_winner]:
            if team not in self.results['finals']:
                self.results['finals'][team] = 0
            self.results['finals'][team] += 1

        _, champ = self.simulate_series(west_winner, east_winner, max(west_semi1_date, west_semi2_date))

        if champ not in self.results['champ']:
            self.results['champ'][champ] = 0
        self.results['champ'][champ] += 1

    
