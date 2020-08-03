import xgboost as xgb
# import datetime
import pickle
import numpy as np
import simulate_season
import datetime

def get_result(results, key, team):
    if team in results[key]:
        return results[key][team]
    return 0

def main():
    with open('players.dictionary', 'rb') as f:
        players = pickle.load(f)

    with open('20players.dictionary', 'rb') as f:
        players_this_season = pickle.load(f)

    with open('20teams.dictionary', 'rb') as f:
        teams = pickle.load(f)

    players_this_postseason = {}
    matchups = {}
    results = {'champ':{}, \
               'finals':{}, \
               'conf':{}, \
               'semi':{}, \
               'playoffs':{}}

    model = xgb.Booster({'nthread': 4})  # init model
    model.load_model('basketball.model')
    lineups = {'LAL':['jamesle01', 'davisan02', 'greenda02', 'caldwke01', 'mcgeeja01', 'kuzmaky01', 'howardw01', 'carusal01', 'cookqu01', 'smithjr01', 'morrima02', 'waitedi01', 'dudleja01'],\
               'LAC':['leonaka01', 'georgpa01', 'morrima03', 'beverpa01', 'zubaciv01', 'shamela01', 'harremo01', 'willilo02', 'jacksre01', 'greenja01', 'mcgruro01', 'noahjo01', 'pattepa01'], \
               'MIL':['antetgi01', 'middlkh01', 'bledser01', 'lopezbr01', 'matthwe02', 'divindo01', 'ilyaser01', 'korveky01', 'lopezro01', 'hillge01', 'connapa01', 'brownst02'], \
               'PHI':['simmobe01', 'harrito02', 'embiijo01', 'richajo01', 'thybuma01', 'horfoal01', 'korkmfu01', 'robingl02', 'burksal01', 'scottmi01', 'netora01', 'miltosh01', 'oquinky01'], \
               'HOU':['hardeja01', 'westbru01', 'tuckepj01', 'covinro01', 'houseda01', 'gordoer01', 'riverau01', 'mclembe01', 'greenje02', 'sefolth01', 'carrode01', 'mbahalu01', 'nwabada01'], \
               'BOS':['walkeke02', 'haywago01', 'tatumja01', 'brownja02', 'theisda01', 'smartma01', 'kanteen01', 'willigr01', 'wanambr01', 'ojelese01', 'williro04'], \
               'TOR':['lowryky01', 'siakapa01', 'anunoog01', 'gasolma01', 'vanvlfr01', 'powelno01', 'ibakase01', 'holliro01', 'daviste02', 'mccawpa01', 'bouchch01', 'thomama02'], \
               'DEN':['jokicni01', 'murraja01', 'harriga01', 'millspa01', 'bartowi01', 'grantje01', 'craigto01', 'morrimo01', 'plumlma01', 'doziepj01', 'bateske01', 'vonleno01', 'portemi01'], \
               'DAL':['doncilu01', 'porzikr01', 'finnedo01', 'hardati02', 'curryse01', 'klebima01', 'wrighde01', 'jacksju01', 'kiddgmi01', 'caulewi01', 'burketr01', 'marjabo01', 'bareajo01'], \
               'OKC':['paulch01', 'gallida01', 'adamsst01', 'gilgesh01', 'dortlu01', 'schrode01', 'fergute01', 'noelne01', 'roberan03', 'bazleda01', 'diallha01', 'naderab01', 'muscami01'], \
               'UTA':['goberru01', 'mitchdo01', 'conlemi01', 'inglejo01', 'onealro01', 'clarkjo01', 'niangge01', 'davised01', 'bradlto01', 'morgaju01', 'brantja01', 'tuckera01'], \
               'MIA':['butleji01', 'adebaba01', 'nunnke01', 'robindu01', 'crowdja01', 'dragigo01', 'herroty01', 'leoname01', 'jonesde02', 'iguodan01', 'olynyke01', 'hillso01'], \
               'IND':['warretj01', 'brogdma01', 'turnemy01', 'oladivi01', 'holidaa01', 'sabondo01', 'holidju01', 'mcderdo01', 'sumneed01', 'mccontj01', 'bitadgo01', 'leaftj01', 'johnsal02'], \
               'POR':['lillada01', 'mccolcj01', 'nurkiju01', 'anthoca01', 'colliza01', 'hoodro01', 'whiteha01', 'trentga02', 'hezonma01', 'simonan01', 'adamsja01', 'littlna01'], \
               'ORL':['vucevni01', 'fournev01', 'gordoaa01', 'augusdj01', 'ennisja01', 'isaacjo01', 'fultzma01', 'rosste01', 'birchkh01', 'cartemi01', 'iwundwe01', 'clarkga01'], \
               'BRK':['allenja01', 'harrijo01', 'leverca01', 'thomala01', 'johnsty01', 'templga01', 'kurucro01', 'anderju01', 'luwawti01', 'musadz01', 'chiozch01', 'martije02'], \
               'MEM':['moranja01', 'jacksja02', 'brookdi01', 'valanjo01', 'anderky01', 'meltode01', 'clarkbr01', 'jacksjo02', 'dienggo01', 'gudurma01', 'tollian01', 'konchjo01', 'watanyu01'], \
               'NOP':['holidjr01', 'ingrabr01', 'willizi01', 'favorde01', 'redicjj01', 'balllo01', 'hartjo01', 'mellini01', 'mooreet01', 'willike04', 'hayesja02', 'okafoja01'], \
               'SAC':['barneha02', 'foxde01', 'bjeline01','holmeri01', 'bogdabo01', 'hieldbu01', 'parkeja01', 'josepco01', 'bazemke01', 'ferreyo01', 'gilesha01', 'lenal01', 'breweco01'], \
               'WAS':['hachiru01', 'bryanth01', 'browntr01', 'napiesh01', 'bongais01', 'smithis01', 'mahinia01', 'wagnemo01', 'robinje01', 'pasecan01', 'paytoga02', 'grantje02', 'schofad01'], \
               'SAS':['derozde01', 'murrade01', 'whitede01', 'poeltja01', 'walkelo01', 'gayru01', 'forbebr01', 'millspa02', 'zellety01', 'belinma01', 'metuch01', 'samanlu01', 'eubandr01'], \
               'PHO':['bookede01', 'aytonde01', 'rubiori01', 'bridgmi01', 'johnsca02', 'saricda01', 'kaminfr01', 'baynear01', 'carteje01', 'payneca01', 'okoboel01', 'diallch01', 'jeromty01']}

    schedule = [{'team1':'UTA', 'team2':'NOP', 'date':datetime.date(2020, 7, 30)},\
                {'team1':'LAC', 'team2':'LAL', 'date':datetime.date(2020, 7, 30)},\
                {'team1':'ORL', 'team2':'BRK', 'date':datetime.date(2020, 7, 31)},\
                {'team1':'PHO', 'team2':'WAS', 'date':datetime.date(2020, 7, 31)},\
                {'team1':'MEM', 'team2':'POR', 'date':datetime.date(2020, 7, 31)},\
                {'team1':'BOS', 'team2':'MIL', 'date':datetime.date(2020, 7, 31)},\
                {'team1':'SAC', 'team2':'SAS', 'date':datetime.date(2020, 7, 31)},\
                {'team1':'DAL', 'team2':'HOU', 'date':datetime.date(2020, 7, 31)},\
                {'team1':'MIA', 'team2':'DEN', 'date':datetime.date(2020, 8, 1)},\
                {'team1':'UTA', 'team2':'OKC', 'date':datetime.date(2020, 8, 1)},\
                {'team1':'NOP', 'team2':'LAC', 'date':datetime.date(2020, 8, 1)},\
                {'team1':'PHI', 'team2':'IND', 'date':datetime.date(2020, 8, 1)},\
                {'team1':'LAL', 'team2':'TOR', 'date':datetime.date(2020, 8, 1)},\
                {'team1':'WAS', 'team2':'BRK', 'date':datetime.date(2020, 8, 2)},\
                {'team1':'POR', 'team2':'BOS', 'date':datetime.date(2020, 8, 2)},\
                {'team1':'SAS', 'team2':'MEM', 'date':datetime.date(2020, 8, 2)},\
                {'team1':'SAC', 'team2':'ORL', 'date':datetime.date(2020, 8, 2)},\
                {'team1':'MIL', 'team2':'HOU', 'date':datetime.date(2020, 8, 2)},\
                {'team1':'DAL', 'team2':'PHO', 'date':datetime.date(2020, 8, 2)},\
                {'team1':'TOR', 'team2':'MIA', 'date':datetime.date(2020, 8, 3)},\
                {'team1':'IND', 'team2':'WAS', 'date':datetime.date(2020, 8, 3)},\
                {'team1':'DEN', 'team2':'OKC', 'date':datetime.date(2020, 8, 3)},\
                {'team1':'MEM', 'team2':'NOP', 'date':datetime.date(2020, 8, 3)},\
                {'team1':'SAS', 'team2':'PHI', 'date':datetime.date(2020, 8, 3)},\
                {'team1':'LAL', 'team2':'UTA', 'date':datetime.date(2020, 8, 3)},\
                {'team1':'BRK', 'team2':'MIL', 'date':datetime.date(2020, 8, 4)},\
                {'team1':'DAL', 'team2':'SAC', 'date':datetime.date(2020, 8, 4)},\
                {'team1':'PHO', 'team2':'LAC', 'date':datetime.date(2020, 8, 4)},\
                {'team1':'ORL', 'team2':'IND', 'date':datetime.date(2020, 8, 4)},\
                {'team1':'BOS', 'team2':'MIA', 'date':datetime.date(2020, 8, 4)},\
                {'team1':'HOU', 'team2':'POR', 'date':datetime.date(2020, 8, 4)},\
                {'team1':'MEM', 'team2':'UTA', 'date':datetime.date(2020, 8, 5)},\
                {'team1':'PHI', 'team2':'WAS', 'date':datetime.date(2020, 8, 5)},\
                {'team1':'DEN', 'team2':'SAS', 'date':datetime.date(2020, 8, 5)},\
                {'team1':'OKC', 'team2':'LAL', 'date':datetime.date(2020, 8, 5)},\
                {'team1':'TOR', 'team2':'ORL', 'date':datetime.date(2020, 8, 5)},\
                {'team1':'BRK', 'team2':'BOS', 'date':datetime.date(2020, 8, 5)},\
                {'team1':'NOP', 'team2':'SAC', 'date':datetime.date(2020, 8, 6)},\
                {'team1':'MIA', 'team2':'MIL', 'date':datetime.date(2020, 8, 6)},\
                {'team1':'IND', 'team2':'PHO', 'date':datetime.date(2020, 8, 6)},\
                {'team1':'LAC', 'team2':'DAL', 'date':datetime.date(2020, 8, 6)},\
                {'team1':'POR', 'team2':'DEN', 'date':datetime.date(2020, 8, 6)},\
                {'team1':'LAL', 'team2':'HOU', 'date':datetime.date(2020, 8, 6)},\
                {'team1':'UTA', 'team2':'SAS', 'date':datetime.date(2020, 8, 7)},\
                {'team1':'OKC', 'team2':'MEM', 'date':datetime.date(2020, 8, 7)},\
                {'team1':'SAC', 'team2':'BRK', 'date':datetime.date(2020, 8, 7)},\
                {'team1':'ORL', 'team2':'PHI', 'date':datetime.date(2020, 8, 7)},\
                {'team1':'WAS', 'team2':'NOP', 'date':datetime.date(2020, 8, 7)},\
                {'team1':'BOS', 'team2':'TOR', 'date':datetime.date(2020, 8, 7)},\
                {'team1':'LAC', 'team2':'POR', 'date':datetime.date(2020, 8, 8)},\
                {'team1':'UTA', 'team2':'DEN', 'date':datetime.date(2020, 8, 8)},\
                {'team1':'LAL', 'team2':'IND', 'date':datetime.date(2020, 8, 8)},\
                {'team1':'PHO', 'team2':'MIA', 'date':datetime.date(2020, 8, 8)},\
                {'team1':'MIL', 'team2':'DAL', 'date':datetime.date(2020, 8, 8)},\
                {'team1':'WAS', 'team2':'OKC', 'date':datetime.date(2020, 8, 9)},\
                {'team1':'MEM', 'team2':'TOR', 'date':datetime.date(2020, 8, 9)},\
                {'team1':'SAS', 'team2':'NOP', 'date':datetime.date(2020, 8, 9)},\
                {'team1':'ORL', 'team2':'BOS', 'date':datetime.date(2020, 8, 9)},\
                {'team1':'PHI', 'team2':'POR', 'date':datetime.date(2020, 8, 9)},\
                {'team1':'HOU', 'team2':'SAC', 'date':datetime.date(2020, 8, 9)},\
                {'team1':'BRK', 'team2':'LAC', 'date':datetime.date(2020, 8, 9)},\
                {'team1':'OKC', 'team2':'PHO', 'date':datetime.date(2020, 8, 10)},\
                {'team1':'DAL', 'team2':'UTA', 'date':datetime.date(2020, 8, 10)},\
                {'team1':'TOR', 'team2':'MIL', 'date':datetime.date(2020, 8, 10)},\
                {'team1':'IND', 'team2':'MIA', 'date':datetime.date(2020, 8, 10)},\
                {'team1':'DEN', 'team2':'LAL', 'date':datetime.date(2020, 8, 10)},\
                {'team1':'BRK', 'team2':'ORL', 'date':datetime.date(2020, 8, 11)},\
                {'team1':'HOU', 'team2':'SAS', 'date':datetime.date(2020, 8, 11)},\
                {'team1':'PHO', 'team2':'PHI', 'date':datetime.date(2020, 8, 11)},\
                {'team1':'POR', 'team2':'DAL', 'date':datetime.date(2020, 8, 11)},\
                {'team1':'BOS', 'team2':'MEM', 'date':datetime.date(2020, 8, 11)},\
                {'team1':'MIL', 'team2':'WAS', 'date':datetime.date(2020, 8, 11)},\
                {'team1':'NOP', 'team2':'SAC', 'date':datetime.date(2020, 8, 11)},\
                {'team1':'IND', 'team2':'HOU', 'date':datetime.date(2020, 8, 12)},\
                {'team1':'TOR', 'team2':'PHI', 'date':datetime.date(2020, 8, 12)},\
                {'team1':'MIA', 'team2':'OKC', 'date':datetime.date(2020, 8, 12)},\
                {'team1':'LAC', 'team2':'DEN', 'date':datetime.date(2020, 8, 12)},\
                {'team1':'SAS', 'team2':'UTA', 'date':datetime.date(2020, 8, 13)},\
                {'team1':'SAC', 'team2':'LAL', 'date':datetime.date(2020, 8, 13)},\
                {'team1':'MIL', 'team2':'MEM', 'date':datetime.date(2020, 8, 13)},\
                {'team1':'WAS', 'team2':'BOS', 'date':datetime.date(2020, 8, 13)},\
                {'team1':'POR', 'team2':'BRK', 'date':datetime.date(2020, 8, 13)},\
                {'team1':'NOP', 'team2':'ORL', 'date':datetime.date(2020, 8, 13)},\
                {'team1':'DAL', 'team2':'PHO', 'date':datetime.date(2020, 8, 13)},\
                {'team1':'PHI', 'team2':'HOU', 'date':datetime.date(2020, 8, 14)},\
                {'team1':'DEN', 'team2':'TOR', 'date':datetime.date(2020, 8, 14)},\
                {'team1':'OKC', 'team2':'LAC', 'date':datetime.date(2020, 8, 14)},\
                {'team1':'MIA', 'team2':'IND', 'date':datetime.date(2020, 8, 14)}]

    for i in range(1, 100001):
        simulation = simulate_season.Simulation(teams, players, players_this_season, players_this_postseason, schedule, model, lineups, matchups, results)
        simulation.simulate_reg_season()
        simulation.simulate_playoffs(datetime.date(2020, 8, 17))
        if i % 50 == 0:
            print(i)
            for matchup in matchups.keys():
                print(matchup[0] + ',' + matchup[1] + ',' + str(matchups[matchup]))

            for team in teams.keys():
                print(team + ',' + str(get_result(results, 'playoffs', team)) + ',' + str(get_result(results, 'semi', team)) + ',' + str(get_result(results, 'conf', team)) + ',' + str(get_result(results, 'finals', team)) + ',' + str(get_result(results, 'champ', team)))

    # print(matchups)
    # print(simulation.results)
    for matchup in matchups.keys():
        print(str(matchup) + ',' + str(matchups[matchup]))

    for team in teams.keys():
        print(team + ',' + str(get_result(results, 'playoffs', team)) + ',' + str(get_result(results, 'semi', team)) + ',' + str(get_result(results, 'conf', team)) + ',' + str(get_result(results, 'finals', team)) + ',' + str(get_result(results, 'champ', team)))

    # results = {'champions':{}\
    #            'finals'\
    #            }

    # model = xgb.Booster({'nthread': 4})  # init model
    # model.load_model('basketball.model')

if __name__ == '__main__':
    main()