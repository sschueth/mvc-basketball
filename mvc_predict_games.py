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
from sklearn.neural_network import MLPRegressor, MLPClassifier
import pickle
from datetime import timedelta
import datetime
from mvc_create_nn_data import create_nn_data, load_boxscores
from mvc_nn_mlp_regression import nn_input_format_to_train

def load_nn():
    db = 'databases/neural-net-model-win-loss-classifier.p'
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
    #year = '2018-19'
    data_db, conf_teams = load_boxscores(year)
    data_avg_db = create_nn_data(data_db,conf_teams,only_most_recent=True)
    home_key = list(data_avg_db[home].keys())
    home_nn_data_inputs = data_avg_db[home][home_key[0]]
    visitor_key = list(data_avg_db[visitor].keys())
    visitor_nn_data_inputs = data_avg_db[visitor][visitor_key[0]]

    #for data_idx in range(0, len(nn_data_game_info)):
    #    this_home = nn_data_game_info[data_idx][1]
    #    this_visitor = nn_data_game_info[data_idx][2]
    #    if home in this_home or  home in this_visitor:
    #        home_nn_data_inputs.append(nn_data_inputs[data_idx])
    #        home_nn_data_outputs.append(nn_data_outputs[data_idx])
    #        home_nn_data_game_info.append(nn_data_game_info[data_idx])
    #    if visitor in this_home or visitor in this_visitor:
    #        visitor_nn_data_inputs.append(nn_data_inputs[data_idx])
    #        visitor_nn_data_outputs.append(nn_data_outputs[data_idx])
    #        visitor_nn_data_game_info.append(nn_data_game_info[data_idx])

    #h_idx = get_idx_most_recent(home_nn_data_game_info)
    #v_idx = get_idx_most_recent(visitor_nn_data_game_info)
    input_fields = ['eFG%','TOV%','ORB%','DRB%','FTf']

    this_game_inputs = []

    for input_field in input_fields: 
        this_game_inputs.append(home_nn_data_inputs['For'][input_field])
    for input_field in input_fields:
        this_game_inputs.append(home_nn_data_inputs['Against'][input_field])
    for input_field in input_fields:
        this_game_inputs.append(visitor_nn_data_inputs['For'][input_field])
    for input_field in input_fields:
        this_game_inputs.append(visitor_nn_data_inputs['Against'][input_field])
    
    x = scaler.transform([this_game_inputs])
    y = nn.predict_log_proba(x)
    winning_team = ''
    winning_conf = False
    winning_log_proba = 0
    conf_lim = 0.999-1
    if y[0][0] > y[0][1]:
        winning_team = visitor
        winning_log_proba = y[0][0]
    else:
        winning_team = home
        winning_log_proba = y[0][1]
    if winning_log_proba > conf_lim:
        winning_conf = True
    
    return winning_team, winning_conf, winning_log_proba

def get_units_to_bet(odds, conf):
    odds_factor = 0
    conf_factor = 0

    if odds > 0:
        if odds >= 300:
            odds_factor = 2
        else:
            odds_factor = odds/200 + 0.5
    else:
        if odds <= -300:
            odds_factor = 0.1
        else:
            odds_factor = 0.9/200*odds + 1.45
    
    conf = -conf
    if conf >= 0.1:
        conf_factor = 0.1
    elif conf <= 0.00001:
        conf_factor = 2
    else:
        conf_factor = -0.42 - 0.208*np.log(conf)
    
    units = conf_factor * odds_factor
    return units



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

        pred_team, conf, log_proba = predict_game(home_team, visitor_team,curr_year, nn, scaler)

        print('\n')
        print('Prediction: ' + pred_team)
        print('Confident? ' + str(conf))
        print('Log Probability: ',log_proba)
        if pred_team == home_team:
            moneyline = float(home_money_line)
        else:
            moneyline = float(visitor_money_line)
        
        bet_units = get_units_to_bet(moneyline, log_proba)
        print('Suggested num of units: ', round(bet_units,2))

        print('\n')
        keep_betting = input('Check another game? [y/n]: ')
        if keep_betting == 'y':
            game_num = game_num + 1
            print('-------------------------------------\n')
        elif keep_betting == 'n':
            betting = False
        else:
            print('Command not recognized.')
            betting = False

if __name__ == '__main__':
    main()