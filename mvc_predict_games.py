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
from mvc_nn_mlp_regression import nn_input_format_to_train

def load_nn():
    db = 'databases/neural-net-model-win-loss.p'
    with open(db,'rb') as pickle_file:
        pickle_data = pickle.load(pickle_file)
    nn = pickle_data[0]
    scaler = pickle_data[1]
    #print('\nData loaded: ' + db+'\n')
    return nn, scaler

def get_idx_most_recent(game_info):
    today = datetime.date.today()
    max_date = game_info[0][0]
    max_idx = 0
    for i_idx in range(0,len(game_info)):
        day = game_info[i_idx][0]
        if day >= max_date and day < today:
            max_date = day
            max_idx = i_idx
    return max_idx
    
def predict_game(home,visitor,year,nn,scaler):
    year = '2018-19'
    nn_data_inputs, nn_data_outputs, nn_data_game_info = nn_input_format_to_train([year],get_last_data=True)
    home_nn_data_inputs = []
    home_nn_data_outputs = []
    home_nn_data_game_info = []
    visitor_nn_data_inputs = []
    visitor_nn_data_outputs = []
    visitor_nn_data_game_info = []

    for data_idx in range(0, len(nn_data_game_info)):
        this_home = nn_data_game_info[data_idx][1]
        this_visitor = nn_data_game_info[data_idx][2]
        if home in this_home or  home in this_visitor:
            home_nn_data_inputs.append(nn_data_inputs[data_idx])
            home_nn_data_outputs.append(nn_data_outputs[data_idx])
            home_nn_data_game_info.append(nn_data_game_info[data_idx])
        if visitor in this_home or visitor in this_visitor:
            visitor_nn_data_inputs.append(nn_data_inputs[data_idx])
            visitor_nn_data_outputs.append(nn_data_outputs[data_idx])
            visitor_nn_data_game_info.append(nn_data_game_info[data_idx])

    h_idx = get_idx_most_recent(home_nn_data_game_info)
    v_idx = get_idx_most_recent(visitor_nn_data_game_info)

    

    confidence = 0
    return confidence

def intro(year):
    print('\n------- Money Valley Conference --------------\n')
    print('Conference teams: \n')
    with open(year+'/conference teams.txt','r') as conf_file:
        line = conf_file.readlines()
        for l in line:
            if '\n' in l:
                l = l.replace('\n','')
            print(l)
    print('\n')

def main():
    curr_year = '2019-20'
    intro(curr_year)
    nn, scaler = load_nn()
    betting = True
    game_num = 1
    
    while betting:
        print('Game #',game_num,'...')
        home_team = input('Home team: ')
        visitor_team = input('Visitor team: ')
        home_money_line = input('Home team ML: ')
        visitor_money_line = input('Visitor team ML: ')

        predict_game(home_team, visitor_team,curr_year, nn, scaler)

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