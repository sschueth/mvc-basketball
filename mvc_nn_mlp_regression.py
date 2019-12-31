#-----------------------------------------------------------------
#   mvc_nn_mlp_regression.py
#   Author: Stephen Schueth
#   Overview:   This file is used to train data sets with the 
#               scikit-learn-neural-network library using multi-
#               layer perceptrons. Additionally, this file is used
#               to predict outcomes of this seasons games.
#-----------------------------------------------------------------

# Import Modules
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import datetime
from datetime import timedelta

def nn_input_format_to_train(years):

    nn_data_inputs = []
    nn_data_outputs = []
    nn_data_games_info = []

    for y_idx in range(0,len(years)):
        year = years[y_idx]
        with open('databases/nn-training-data-inputs-'+year+'.p','rb') as pickle_file:
            nn_data = pickle.load(pickle_file)
        
        with open('databases/box-score-dict-'+year+'.p','rb') as pickle_file:
            bs_data = pickle.load(pickle_file)
        
        day_delta = timedelta(days = 1)
        max_day_delta_iter = 14
        nn_input_fields = ['eFG%','TOV%','ORB%','DRB%','FTf']
        nn_output_fields = ['Home +/-','Home W/L','Total O/U']


        for idx in range(0,len(bs_data)):
            home_team = bs_data[idx]['Home']['Team']
            visitor_team = bs_data[idx]['Visitor']['Team']
            d = datetime.date(day=int(bs_data[idx]['Day']),month=int(bs_data[idx]['Month']),year=int(bs_data[idx]['Year']))
            
            if visitor_team == 'SE Missouri State':
                visitor_team = 'Missouri State'
            if home_team == 'SE Missouri State':
                home_team = 'Missouri State'

            if visitor_team == 'Loyola Chicago' and (year == '2016-17' or year == '2018-19' or '2019-20'):
                visitor_team = 'Loyola'
            if home_team == 'Loyola Chicago' and (year == '2016-17' or year == '2018-19' or '2019-20'):
                home_team = 'Loyola'

            home_nn_data = nn_data[home_team]
            visitor_nn_data = nn_data[visitor_team]

            has_nn_data_before_game = False
            home_has_nn_data_before_game = False
            visitor_has_nn_data_before_game = False
            delta_iter = 0
            home_nn_date_to_use = d
            visitor_nn_date_to_use = d

            while delta_iter < max_day_delta_iter and has_nn_data_before_game == False:
                if home_has_nn_data_before_game == False:
                    home_nn_date_to_use = home_nn_date_to_use - day_delta
                    if home_nn_date_to_use in home_nn_data:
                        home_has_nn_data_before_game = True
                if visitor_has_nn_data_before_game == False:
                    visitor_nn_date_to_use = visitor_nn_date_to_use - day_delta
                    if visitor_nn_date_to_use in visitor_nn_data:
                        visitor_has_nn_data_before_game = True
                if home_has_nn_data_before_game and visitor_has_nn_data_before_game:
                    has_nn_data_before_game = True
                delta_iter = delta_iter + 1

            if has_nn_data_before_game == True:
                this_game_inputs = []
                this_game_outputs = []
                for input_field in nn_input_fields:
                    this_game_inputs.append( home_nn_data[home_nn_date_to_use]['For'][input_field] )
                for input_field in nn_input_fields:
                    this_game_inputs.append( home_nn_data[home_nn_date_to_use]['Against'][input_field] )
                for input_field in nn_input_fields:
                    this_game_inputs.append( visitor_nn_data[visitor_nn_date_to_use]['For'][input_field] )
                for input_field in nn_input_fields:
                    this_game_inputs.append( visitor_nn_data[visitor_nn_date_to_use]['Against'][input_field] )
                
                #for output_field in nn_output_fields:
                #    this_game_outputs.append( bs_data[idx][output_field] )
                this_game_outputs = bs_data[idx]['Home W/L']

                this_game_info = [d,home_team,visitor_team]

                nn_data_inputs.append(this_game_inputs)
                nn_data_outputs.append(this_game_outputs)
                nn_data_games_info.append(this_game_info)
            #print(idx)
    return nn_data_inputs, nn_data_outputs, nn_data_games_info

def create_nn(x_data,y_data):
    #nn = MLPRegressor(hidden_layer_sizes=(20,20,),activation='logistic',learning_rate='adaptive',tol=1e-20,solver='adam',max_iter=50000,verbose=True)
    nn = MLPClassifier(hidden_layer_sizes=(20,20,),activation='logistic',learning_rate='adaptive',tol=1e-20,solver='adam',max_iter=50000,verbose=True)
    n = nn.fit(x_data,y_data)
    return n
    
def run_nn(n,x_data):
    #y_predict = n.predict(x_data)
    y_predict = n.predict_log_proba(x_data)
    return y_predict

def split_data_train_and_test(x_data,y_data,split_pct):
    x_train = []
    y_train = []
    x_test = []
    y_test = []

    data_length = len(x_data)
    split_idx = int(data_length*split_pct)
    idx_range = np.arange(0,data_length)
    idx_range = np.random.permutation(idx_range)
    for idx in range(0,split_idx):
        x_train.append(x_data[idx_range[idx]]) 
        y_train.append(y_data[idx_range[idx]])
    for idx in range(split_idx,data_length):
        x_test.append(x_data[idx_range[idx]])
        y_test.append(y_data[idx_range[idx]])
    return x_train, y_train, x_test, y_test

def nn_normalize_data(x_train,x_test):
    scaler = StandardScaler(copy=True,with_mean=True,with_std=True)
    scaler.fit(x_train)
    x_train_norm = scaler.transform(x_train)
    x_test_norm = scaler.transform(x_test)

    #y_spread = []
    #y_winloss = []
    #y_overunder = []
    #for idx in range(0,len(y_data)):
    #    y_spread.append(y_data[idx][0])
    #    y_winloss.append(y_data[idx][1])
    #    y_overunder.append(y_data[idx][2])
    
    #y_spread_norm, spread_norm = preprocessing.normalize(y_spread,return_norm = True)
    #y_winloss_norm, winloss_norm = preprocessing.normalize(y_winloss,return_norm = True)
    #y_overunder_norm, overunder_norm = preprocessing.normalize(y_overunder,return_norm = True)

    #print(y_spread_norm)
    #print(y_data)
    #print(y_norm)
    return x_train_norm, x_test_norm, scaler

def main():
    years = ['2015-16','2016-17','2017-18','2018-19','2019-20']
    #years = ['2016-17','2017-18','2018-19']
    #years = ['2017-18']
    split_pct = 0.8
    x,y,info = nn_input_format_to_train(years)
    x_train,y_train,x_test,y_test = split_data_train_and_test(x,y,split_pct)
    x_train_norm, x_test_norm, scaler = nn_normalize_data(x_train,x_test)
    nn_model = create_nn(x_train_norm,y_train)
    y_predict = run_nn(nn_model, x_test_norm)

    p_file_name = 'databases/neural-net-model-win-loss-classifier.p' 
    with open(p_file_name,'wb') as pickle_file:
        pickle.dump([nn_model, scaler],pickle_file)
    
    #print(len(x))
    #print(len(y))
    print('Actual vs Predicted')
    num_right = 0
    num_wrong = 0
    conf_num_right = 0
    conf_num_wrong = 0
    conf_lim = 0.999 - 1
    for i in range(0,len(y_test)):
        #print('+/-: ',y_test[i][0],' vs ',y_predict[i][0])
        #print('W/L: ',y_test[i][1],' vs ',y_predict[i][1])
        #print('O/U: ',y_test[i][2],' vs ',y_predict[i][2])
        
        if (y_predict[i][0] > y_predict[i][1]):
            y_predict_val = 0
        else:
            y_predict_val = 1
        #y_predict_val = y_predict[i][1]
        #
        
        if y_test[i] == 1:
            if y_predict_val >= 0.5:
                y_predict_prob = y_predict[i][1]
                num_right = num_right + 1
                if y_predict_prob >= conf_lim:
                    conf_num_right = conf_num_right + 1
            else:
                y_predict_prob = y_predict[i][0]
                num_wrong = num_wrong + 1
                if y_predict_prob >= conf_lim:
                    conf_num_wrong = conf_num_wrong + 1
        else:
            
            if y_predict_val < 0.5:
                y_predict_prob = y_predict[i][0]
                num_right = num_right + 1
                if y_predict_prob >= conf_lim:
                    conf_num_right = conf_num_right + 1

            else:
                y_predict_prob = y_predict[i][1]
                num_wrong = num_wrong + 1
                if y_predict_prob >= conf_lim:
                    conf_num_wrong = conf_num_wrong + 1
        print('+/-: ',y_test[i],' vs ',y_predict_val,' (',y_predict_prob,')')

    print('Prediction record: ',num_right,'-',num_wrong)
    print('Confident Pred rec: ',conf_num_right,'-',conf_num_wrong)        
    print('Saved: '+p_file_name)

if __name__ == '__main__':
    main()