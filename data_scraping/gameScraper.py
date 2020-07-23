from bs4 import BeautifulSoup as bsoup
import urllib.request

class Game:
    def __init__(self):
        self.home_team = None
        self.away_team = None
        self.home_starters = []
        self.home_bench = []
        self.away_starters = []
        self.away_bench = []
        self.is_playoff_game = False
        self.result = 0

class StatLine:
    def __init__(self):
        self.tag = None
        self.two_pt_attempts = 0
        self.two_pt_made = 0
        self.three_pt_attempts = 0
        self.three_pt_made = 0
        self.fta = 0
        self.ft = 0
        self.tov = 0
        self.drb = 0
        self.orb = 0
        self.stl = 0
        self.blk = 0
        self.ast = 0
        self.pf = 0
        self.min = 0

def scrapeGame(year, month, day, team):
    game = Game()
    myUrl = 'https://www.basketball-reference.com/boxscores/' \
             + year + month + day + '0' + team + '.html'

    client = urllib.request.urlopen(myUrl).read()
    soup = bsoup(client, 'lxml')
    body = soup.body

    other_scores = body.find(id='other_scores_link')
    game.is_playoff_game = ("Series" in other_scores.get('data-label'))

    div = body.find('div', {'class' : 'content_grid'}) # this is the table
    # before the table for the away team players
    awayTable = div.next_sibling.next_sibling.next_sibling
    game.away_team = awayTable['class'][1][-3:]
    game.home_team = team

    score = 0
    row = awayTable.find_next('tbody').find_next('tr') # first row
    for _ in range(5):
        player = row.find_next(scope = 'row')
        stat_line = StatLine()
        stat_line.playertag = player.get('data-append-csv')

        time = player.find_next('td').string
        seconds = int(time[-2:]) # isolate seconds and minutes
        minutes = int(time[:-3])
        stat_line.min = minutes + seconds / 60

        score -= int(row.find_next('td', {'data-stat' : 'plus_minus'}).text)

        stat_line.three_pt_attempts = int(row.find_next('td', {'data-stat' : 'fg3a'}).text)
        stat_line.three_pt_made = int(row.find_next('td', {'data-stat' : 'fg3'}).text)
        stat_line.two_pt_attempts = int(row.find_next('td', {'data-stat' : 'fga'}).text) - stat_line.three_pt_attempts
        stat_line.two_pt_made = int(row.find_next('td', {'data-stat' : 'fg'}).text) - stat_line.three_pt_made
        stat_line.fta = int(row.find_next('td', {'data-stat' : 'fta'}).text)
        stat_line.ft = int(row.find_next('td', {'data-stat' : 'ft'}).text)
        stat_line.orb = int(row.find_next('td', {'data-stat' : 'orb'}).text)
        stat_line.drb = int(row.find_next('td', {'data-stat' : 'drb'}).text)
        stat_line.ast = int(row.find_next('td', {'data-stat' : 'ast'}).text)
        stat_line.stl = int(row.find_next('td', {'data-stat' : 'stl'}).text)
        stat_line.blk = int(row.find_next('td', {'data-stat' : 'blk'}).text)
        stat_line.tov = int(row.find_next('td', {'data-stat' : 'tov'}).text)
        stat_line.pf = int(row.find_next('td', {'data-stat' : 'pf'}).text)

        game.away_starters.append(stat_line)
        row = row.next_sibling.next_sibling # next row
    row = row.next_sibling.next_sibling # skip a line that isn't a player
    while(row != None): # do the same for the bench players
        player = row.find_next( scope = 'row' )
        stat_line = StatLine()
        stat_line.playertag = player.get('data-append-csv')
        time = player.find_next('td').string

        if 'Not' in time:
            break
        seconds = int(time[-2:])
        minutes = int(time[:-3])
        stat_line.min = minutes + seconds / 60

        score -= int(row.find_next('td', {'data-stat' : 'plus_minus'}).text)

        stat_line.three_pt_attempts = int(row.find_next('td', {'data-stat' : 'fg3a'}).text)
        stat_line.three_pt_made = int(row.find_next('td', {'data-stat' : 'fg3'}).text)
        stat_line.two_pt_attempts = int(row.find_next('td', {'data-stat' : 'fga'}).text) - stat_line.three_pt_attempts
        stat_line.two_pt_made = int(row.find_next('td', {'data-stat' : 'fg'}).text) - stat_line.three_pt_made
        stat_line.fta = int(row.find_next('td', {'data-stat' : 'fta'}).text)
        stat_line.ft = int(row.find_next('td', {'data-stat' : 'ft'}).text)
        stat_line.orb = int(row.find_next('td', {'data-stat' : 'orb'}).text)
        stat_line.drb = int(row.find_next('td', {'data-stat' : 'drb'}).text)
        stat_line.ast = int(row.find_next('td', {'data-stat' : 'ast'}).text)
        stat_line.stl = int(row.find_next('td', {'data-stat' : 'stl'}).text)
        stat_line.blk = int(row.find_next('td', {'data-stat' : 'blk'}).text)
        stat_line.tov = int(row.find_next('td', {'data-stat' : 'tov'}).text)
        stat_line.pf = int(row.find_next('td', {'data-stat' : 'pf'}).text)

        game.away_bench.append(stat_line)
        row = row.next_sibling.next_sibling

    game.result = score / 5
    print(game.result)
    homeTable = awayTable.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
    homeTable = homeTable.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
    row = homeTable.find_next('tbody').find_next('tr')
    for _ in range(5):
        player = row.find_next(scope = 'row')
        stat_line = StatLine()
        stat_line.playertag = player.get('data-append-csv')

        time = player.find_next('td').string
        seconds = int(time[-2:]) # isolate seconds and minutes
        minutes = int(time[:-3])
        stat_line.min = minutes + seconds / 60

        stat_line.three_pt_attempts = int(row.find_next('td', {'data-stat' : 'fg3a'}).text)
        stat_line.three_pt_made = int(row.find_next('td', {'data-stat' : 'fg3'}).text)
        stat_line.two_pt_attempts = int(row.find_next('td', {'data-stat' : 'fga'}).text) - stat_line.three_pt_attempts
        stat_line.two_pt_made = int(row.find_next('td', {'data-stat' : 'fg'}).text) - stat_line.three_pt_made
        stat_line.fta = int(row.find_next('td', {'data-stat' : 'fta'}).text)
        stat_line.ft = int(row.find_next('td', {'data-stat' : 'ft'}).text)
        stat_line.orb = int(row.find_next('td', {'data-stat' : 'orb'}).text)
        stat_line.drb = int(row.find_next('td', {'data-stat' : 'drb'}).text)
        stat_line.ast = int(row.find_next('td', {'data-stat' : 'ast'}).text)
        stat_line.stl = int(row.find_next('td', {'data-stat' : 'stl'}).text)
        stat_line.blk = int(row.find_next('td', {'data-stat' : 'blk'}).text)
        stat_line.tov = int(row.find_next('td', {'data-stat' : 'tov'}).text)
        stat_line.pf = int(row.find_next('td', {'data-stat' : 'pf'}).text)

        game.home_starters.append(stat_line)
        row = row.next_sibling.next_sibling # next row
    row = row.next_sibling.next_sibling # skip a line that isn't a player
    while(row != None): # do the same for the bench players
        player = row.find_next( scope = 'row' )
        stat_line = StatLine()
        stat_line.playertag = player.get('data-append-csv')
        time = player.find_next('td').string

        if 'Not' in time:
            break
        seconds = int(time[-2:])
        minutes = int(time[:-3])
        stat_line.min = minutes + seconds / 60

        stat_line.three_pt_attempts = int(row.find_next('td', {'data-stat' : 'fg3a'}).text)
        stat_line.three_pt_made = int(row.find_next('td', {'data-stat' : 'fg3'}).text)
        stat_line.two_pt_attempts = int(row.find_next('td', {'data-stat' : 'fga'}).text) - stat_line.three_pt_attempts
        stat_line.two_pt_made = int(row.find_next('td', {'data-stat' : 'fg'}).text) - stat_line.three_pt_made
        stat_line.fta = int(row.find_next('td', {'data-stat' : 'fta'}).text)
        stat_line.ft = int(row.find_next('td', {'data-stat' : 'ft'}).text)
        stat_line.orb = int(row.find_next('td', {'data-stat' : 'orb'}).text)
        stat_line.drb = int(row.find_next('td', {'data-stat' : 'drb'}).text)
        stat_line.ast = int(row.find_next('td', {'data-stat' : 'ast'}).text)
        stat_line.stl = int(row.find_next('td', {'data-stat' : 'stl'}).text)
        stat_line.blk = int(row.find_next('td', {'data-stat' : 'blk'}).text)
        stat_line.tov = int(row.find_next('td', {'data-stat' : 'tov'}).text)
        stat_line.pf = int(row.find_next('td', {'data-stat' : 'pf'}).text)

        game.home_bench.append(stat_line)
        row = row.next_sibling.next_sibling

    
    return game
        