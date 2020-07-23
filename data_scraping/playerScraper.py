from bs4 import BeautifulSoup as bsoup
import urllib.request

def scrapePlayer(player):
    myUrl = 'https://www.basketball-reference.com/players/' + \
            player[0] + '/' + player + '.html'

    player = {}

    client = urllib.request.urlopen(myUrl).read()
    soup = bsoup(client, 'lxml')
    body = soup.body
    # "working" is what I will call the html object that I am currently 
    # working with when I do not know what else to call it.
    working = body.find(id='meta')
    working = working.find_next('span').find_next('span')
    height = working.text.split('-')
    player['height'] = int(height[0])*12 + int(height[1])
    working = working.next_sibling.next_sibling
    player['weight'] = int(working.text[:-2])
    working = working.find_next('span')
    player['birthday'] = working['data-birth']

    # working = body.find(id = 'all_per_game')
    # working = working.find_next('div').next_sibling.next_sibling.next_sibling.next_sibling
    # working = str(working)
    # newSoup = bsoup(working, 'lxml')
    # newBody = newSoup.body
    # tableBody = newBody.find('tbody')
    working = body.find(id = 'per_game')
    working = working.find_next('tbody')
    tableRow = working.find_next('tr')
    fga = {}
    years_seen = set()
    while(tableRow != None):
        if tableRow.get('id') != None and tableRow.get('id')[-2:] not in years_seen:
            stats = []
            stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'g'}).text) / 82, 3))
            stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'gs'}).text) / 82, 3))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'mp_per_g'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'orb_per_g'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'drb_per_g'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'ast_per_g'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'blk_per_g'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'stl_per_g'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'tov_per_g'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'pf_per_g'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'fta_per_g'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'ft_pct'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'fg3_per_g'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'fg3_pct'}).text))
            year = tableRow['id'][-2:]
            fga[year] = (float(tableRow.find_next('td', {'data-stat' : 'fga_per_g'}).text))
            player[year] = stats
            years_seen.add(year)
        tableRow = tableRow.next_sibling.next_sibling

    div = body.find(id = 'all_shooting')
    div = div.find_next('div').next_sibling.next_sibling.next_sibling.next_sibling
    strTable = str(div)
    newSoup = bsoup(strTable, 'lxml')
    newBody = newSoup.body
    tableBody = newBody.find('tbody')
    tableRow = tableBody.find_next('tr')
    years_seen = set()
    while(tableRow != None):
        if tableRow.get('id') != None and tableRow.get('id')[-2:] not in years_seen:
            stats = []
            year = tableRow['id'][-2:]
            stats.append(fga[year] * float(tableRow.find_next('td', {'data-stat' : 'pct_fga_16_xx'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'fg_pct_16_xx'}).text))
            stats.append(fga[year] * float(tableRow.find_next('td', {'data-stat' : 'pct_fga_10_16'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'fg_pct_10_16'}).text))
            stats.append(fga[year] * float(tableRow.find_next('td', {'data-stat' : 'pct_fga_03_10'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'fg_pct_03_10'}).text))
            stats.append(fga[year] * float(tableRow.find_next('td', {'data-stat' : 'pct_fga_00_03'}).text))
            stats.append(float(tableRow.find_next('td', {'data-stat' : 'fg_pct_00_03'}).text))
            player[year] += stats
            years_seen.add(year)
        tableRow = tableRow.next_sibling.next_sibling

    div = body.find(id = 'all_playoffs_per_game')
    div = div.find_next('div').next_sibling.next_sibling.next_sibling.next_sibling
    strTable = str(div)
    newSoup = bsoup(strTable, 'lxml')
    newBody = newSoup.body
    tableBody = newBody.find('tbody')
    tableRow = tableBody.find_next('tr')
    playoff_fga = {}
    while(tableRow != None):
        stats = []
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'g'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'gs'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'mp_per_g'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'orb_per_g'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'drb_per_g'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'ast_per_g'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'blk_per_g'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'stl_per_g'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'tov_per_g'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'pf_per_g'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'fta_per_g'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'ft_pct'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'fg3_per_g'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'fg3_pct'}).text))
        year = tableRow['id'][-2:]
        playoff_fga[year] = (float(tableRow.find_next('td', {'data-stat' : 'fga_per_g'}).text))
        player['playoff' + year] = stats
        tableRow = tableRow.next_sibling.next_sibling

    div = body.find(id = 'all_playoffs_shooting')
    div = div.find_next('div').next_sibling.next_sibling.next_sibling.next_sibling
    strTable = str(div)
    newSoup = bsoup(strTable, 'lxml')
    newBody = newSoup.body
    tableBody = newBody.find('tbody')
    tableRow = tableBody.find_next('tr')
    while(tableRow != None):
        stats = []
        year = tableRow['id'][-2:]
        stats.append(playoff_fga[year] * float(tableRow.find_next('td', {'data-stat' : 'pct_fga_16_xx'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'fg_pct_16_xx'}).text))
        stats.append(playoff_fga[year] * float(tableRow.find_next('td', {'data-stat' : 'pct_fga_10_16'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'fg_pct_10_16'}).text))
        stats.append(playoff_fga[year] * float(tableRow.find_next('td', {'data-stat' : 'pct_fga_03_10'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'fg_pct_03_10'}).text))
        stats.append(playoff_fga[year] * float(tableRow.find_next('td', {'data-stat' : 'pct_fga_00_03'}).text))
        stats.append(float(tableRow.find_next('td', {'data-stat' : 'fg_pct_00_03'}).text))
        player['playoff' + year] += stats
        tableRow = tableRow.next_sibling.next_sibling

    return player