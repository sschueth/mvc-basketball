#-------------------------------------------------------------
#   mvc_predict_games.py
#   Author: Stephen Schueth
#   Overview:   This file uses the trained neural network to 
#               predict the outcome of Missouri Valley 
#               Conference basketball games.
#-------------------------------------------------------------

# Import Modules
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import pickle
from datetime import timedelta
import datetime


def load_nn():
    db = 'databases/neural-net-model-win-loss.p'
    with open(db,'rb') as pickle_file:
        pickle_data = pickle.load(pickle_file)
    nn = pickle_data[0]
    scaler = pickle_data[1]
    print('Pickle data loaded: ' + db)
    return nn, scaler



def main():
    nn, scaler = load_nn()
    betting = True
    game_num = 1
    while betting:
        print('Game #',game_num,'...')
        home_team = input('Home team: ')
        visitor_team = input('Visitor team: ')
        home_money_line = input('Home team ML: ')
        visitor_money_line = input('Visitor team ML: ')
        print('\n\n')
        print('Some prediction and why...')
        print('\n\n')
        keep_betting = input('Check another game? [y/n] \n')
        if keep_betting == 'y':
            game_num = game_num + 1
            print('\n\n\n')
        elif keep_betting == 'n':
            betting = False
        else:
            print('Command not recognized.')
            betting = False

if __name__ == '__main__':
    main()