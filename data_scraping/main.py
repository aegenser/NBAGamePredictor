import seasonScraper
import pickle
import numpy as np

def main():
    try:
        with open('players.dictionary', 'rb') as f:
            players = pickle.load(f)
    except:
        players = {}

    data = []

    for ss in ['05' , '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']:
        seasonScraper.scrapeSeasonV2(players, ss, data)
        np.savetxt('data_small.csv', data, delimiter=',')
        with open('players.dictionary', 'wb') as f:
            pickle.dump(players, f)
        

if __name__ == '__main__':
    main()