from bs4 import BeautifulSoup as bsoup
import urllib.request
import datetime
import constant

def safe_float(s):
    if len(s) == 0:
        return 0.0
    else:
        return float(s)

def scrapePlayer(player):
    print("scraping player: " + player)
    myUrl = 'https://www.basketball-reference.com/players/' + \
            player[0] + '/' + player + '.html'

    player = {}
    
    client = urllib.request.urlopen(myUrl).read()
    soup = bsoup(client, 'lxml')
    body = soup.body
    # "working" is what I will call the html object that I am currently 
    # working with when I do not know what else to call it.
    working = body.find(id='meta')
    working = working.find_next('span')
    while('itemprop' not in working.attrs):
        working = working.find_next('span')
    height = working.text.split('-')
    player['height'] = int(height[0])*12 + int(height[1])
    working = working.next_sibling.next_sibling
    player['weight'] = int(working.text[:-2])
    working = working.find_next('span')
    player['birthday'] = datetime.date(int(working['data-birth'][0:4]), int(working['data-birth'][5:7]), int(working['data-birth'][8:10]))
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
            stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'g'}).text) / constant.G_SCLR, 3))
            stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'gs'}).text) / constant.G_SCLR, 3))
            stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'mp_per_g'}).text) / constant.MP_SCLR, 3))
            stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'orb_per_g'}).text) / constant.ORB_SCLR, 3))
            stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'drb_per_g'}).text) / constant.DRB_SCLR, 3))
            stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'ast_per_g'}).text) / constant.AST_SCLR, 3))
            stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'blk_per_g'}).text) / constant.BLK_SCLR, 3))
            stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'stl_per_g'}).text) / constant.STL_SCLR, 3))
            stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'tov_per_g'}).text) / constant.TOV_SCLR, 3))
            stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'pf_per_g'}).text) / constant.PF_SCLR, 3))
            stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fta_per_g'}).text) / constant.FTA_SCLR, 3))
            stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'ft_pct'}).text), 3))
            stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fg3_per_g'}).text) / constant.FG3A_SCLR, 3))
            stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fg3_pct'}).text), 3))
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
            stats.append(round(fga[year] * safe_float(tableRow.find_next('td', {'data-stat' : 'pct_fga_16_xx'}).text) / constant.FG16_XXA_SCLR, 3))
            stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fg_pct_16_xx'}).text), 3))
            stats.append(round(fga[year] * safe_float(tableRow.find_next('td', {'data-stat' : 'pct_fga_10_16'}).text) / constant.FG10_16A_SCLR, 3))
            stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fg_pct_10_16'}).text), 3))
            stats.append(round(fga[year] * safe_float(tableRow.find_next('td', {'data-stat' : 'pct_fga_03_10'}).text) / constant.FG3_10A_SCLR, 3))
            stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fg_pct_03_10'}).text), 3))
            stats.append(round(fga[year] * safe_float(tableRow.find_next('td', {'data-stat' : 'pct_fga_00_03'}).text) / constant.FG0_3A_SCLR, 3))
            stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fg_pct_00_03'}).text), 3))
            player[year] += stats
            years_seen.add(year)
        tableRow = tableRow.next_sibling.next_sibling

    div = body.find(id = 'all_playoffs_per_game')
    if div == None:
        return player
    div = div.find_next('div').next_sibling.next_sibling.next_sibling.next_sibling
    strTable = str(div)
    newSoup = bsoup(strTable, 'lxml')
    newBody = newSoup.body
    tableBody = newBody.find('tbody')
    tableRow = tableBody.find_next('tr')
    playoff_fga = {}
    while(tableRow != None):
        stats = []
        stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'g'}).text) / constant.G_SCLR, 3))
        stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'gs'}).text) / constant.G_SCLR, 3))
        stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'mp_per_g'}).text) / constant.MP_SCLR, 3))
        stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'orb_per_g'}).text) / constant.ORB_SCLR, 3))
        stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'drb_per_g'}).text) / constant.DRB_SCLR, 3))
        stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'ast_per_g'}).text) / constant.AST_SCLR, 3))
        stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'blk_per_g'}).text) / constant.BLK_SCLR, 3))
        stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'stl_per_g'}).text) / constant.STL_SCLR, 3))
        stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'tov_per_g'}).text) / constant.TOV_SCLR, 3))
        stats.append(round(float(tableRow.find_next('td', {'data-stat' : 'pf_per_g'}).text) / constant.PF_SCLR, 3))
        stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fta_per_g'}).text) / constant.FTA_SCLR, 3))
        stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'ft_pct'}).text), 3))
        stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fg3_per_g'}).text) / constant.FG3A_SCLR, 3))
        stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fg3_pct'}).text), 3))
        year = tableRow['id'][-2:]
        playoff_fga[year] = (float(tableRow.find_next('td', {'data-stat' : 'fga_per_g'}).text))
        player['playoff' + year] = stats
        tableRow = tableRow.next_sibling.next_sibling

    div = body.find(id = 'all_playoffs_shooting')
    if div == None:
        return player
    div = div.find_next('div').next_sibling.next_sibling.next_sibling.next_sibling
    strTable = str(div)
    newSoup = bsoup(strTable, 'lxml')
    newBody = newSoup.body
    tableBody = newBody.find('tbody')
    tableRow = tableBody.find_next('tr')
    while(tableRow != None):
        stats = []
        year = tableRow['id'][-2:]
        stats.append(round(playoff_fga[year] * safe_float(tableRow.find_next('td', {'data-stat' : 'pct_fga_16_xx'}).text) / constant.FG16_XXA_SCLR, 3))
        stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fg_pct_16_xx'}).text), 3))
        stats.append(round(playoff_fga[year] * safe_float(tableRow.find_next('td', {'data-stat' : 'pct_fga_10_16'}).text) / constant.FG10_16A_SCLR, 3))
        stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fg_pct_10_16'}).text), 3))
        stats.append(round(playoff_fga[year] * safe_float(tableRow.find_next('td', {'data-stat' : 'pct_fga_03_10'}).text) / constant.FG3_10A_SCLR, 3))
        stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fg_pct_03_10'}).text), 3))
        stats.append(round(playoff_fga[year] * safe_float(tableRow.find_next('td', {'data-stat' : 'pct_fga_00_03'}).text) / constant.FG0_3A_SCLR, 3))
        stats.append(round(safe_float(tableRow.find_next('td', {'data-stat' : 'fg_pct_00_03'}).text), 3))
        player['playoff' + year] += stats
        tableRow = tableRow.next_sibling.next_sibling

    # except:
    #     return player

    return player