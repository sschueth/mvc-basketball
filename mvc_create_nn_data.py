import numpy as np
import pickle
import datetime




def load_boxscores(year):
    # Load pickle database with box scores
    pickle_db = 'databases/box-score-dict-'+year+'.p'
    with open(pickle_db,'rb') as pick_file:
        data_db = pickle.load(pick_file)

    # Load file with list of conference teams
    with open(year+'/conference teams.txt','r') as conf_teams_file:
        conf_team_file = conf_teams_file.readlines()

    conf_teams = []
    for c in conf_team_file:
        if '\n' in c:
            c = c.replace('\n','')
        conf_teams.append(c)

    return data_db, conf_teams



def create_nn_data(data_db, conf_teams,only_most_recent = False):
    # List of fields in the box score database
    box_score_fields = ['FG','FGA','3FG','3FGA','FT','FTA','ORB','DRB','REB','PF','TP','A','TO','BLK','S']

    # Empty NN inputs database
    data_avg_db = {}

    # Iterate through each team in the conference
    for team in conf_teams:
    
        # Initialize each conference teams NN inputs database
        data_avg_db[team] = {}

        # Empty lists that index this teams games and when they were played
        this_team_idx_list = []
        this_date_list = []
        this_team_home_list = []

        # Iterate through all the box scores of all conference teams
        for idx in range(0,len(data_db)):
        
            # Store when this team played, whether they were home or not, and it's index in lists
            if team in data_db[idx]['Home']['Team']:
                this_team_idx_list.append(idx)
                this_date_list.append(datetime.date(month = int(data_db[idx]['Month']), day = int(data_db[idx]['Day']), year = int(data_db[idx]['Year'])))
                this_team_home_list.append(1)
            if team in data_db[idx]['Visitor']['Team']:
                this_team_idx_list.append(idx)
                this_date_list.append(datetime.date(month = int(data_db[idx]['Month']), day = int(data_db[idx]['Day']), year = int(data_db[idx]['Year'])))
                this_team_home_list.append(0)
        
        len_list = len(this_team_idx_list)
        # Compile all box scores up to a certain date in the new NN inputs database
        while len_list > 0:
        
            # Find the latest date (in the remaining list) that this team played
            max_date = this_date_list[0]
            max_date_idx = 0
            for j in range(0,len(this_date_list)):
                if this_date_list[j] > max_date:
                    max_date = this_date_list[j]
                    max_date_idx = j
        
            # Initialize NN inputs data for this team at this date
            data_avg_db[team][max_date] = {}
            data_avg_db[team][max_date]['For'] = {}
            data_avg_db[team][max_date]['Against'] = {}
            for i in range(0,len(box_score_fields)):
                data_avg_db[team][max_date]['For'][box_score_fields[i]] = 0
                data_avg_db[team][max_date]['Against'][box_score_fields[i]] = 0
        
            # Add box score summation (totals) up to this date in the NN inputs databse
            for i in range(0,len(this_team_idx_list)):
                if this_team_home_list[i] == 1:
                    for field in box_score_fields:
                        data_avg_db[team][max_date]['For'][field] = data_avg_db[team][max_date]['For'][field] + data_db[this_team_idx_list[i]]['Home'][field]
                        data_avg_db[team][max_date]['Against'][field] = data_avg_db[team][max_date]['Against'][field] + data_db[this_team_idx_list[i]]['Visitor'][field]
                else:
                    for field in box_score_fields:   
                        data_avg_db[team][max_date]['For'][field] = data_avg_db[team][max_date]['For'][field] + data_db[this_team_idx_list[i]]['Visitor'][field]
                        data_avg_db[team][max_date]['Against'][field] = data_avg_db[team][max_date]['Against'][field] + data_db[this_team_idx_list[i]]['Home'][field]
        
            # Add Dean Oliver's "Four Factors of Success in Basketball" into the NN inputs database
            # For this team
            data_avg_db[team][max_date]['For']['eFG%'] = ( data_avg_db[team][max_date]['For']['FG'] + 0.5*data_avg_db[team][max_date]['For']['3FG'] )/ data_avg_db[team][max_date]['For']['FGA']
            data_avg_db[team][max_date]['For']['TOV%'] = data_avg_db[team][max_date]['For']['TO'] / (data_avg_db[team][max_date]['For']['FGA'] + 0.44*data_avg_db[team][max_date]['For']['FTA'] + data_avg_db[team][max_date]['For']['TO'])
            data_avg_db[team][max_date]['For']['ORB%'] = data_avg_db[team][max_date]['For']['ORB'] / (data_avg_db[team][max_date]['Against']['DRB'] + data_avg_db[team][max_date]['For']['ORB'])
            data_avg_db[team][max_date]['For']['DRB%'] = data_avg_db[team][max_date]['For']['DRB'] / (data_avg_db[team][max_date]['For']['DRB'] + data_avg_db[team][max_date]['Against']['ORB'])
            data_avg_db[team][max_date]['For']['FTf'] = data_avg_db[team][max_date]['For']['FT']/data_avg_db[team][max_date]['For']['FGA']
            # Against this team
            data_avg_db[team][max_date]['Against']['eFG%'] = ( data_avg_db[team][max_date]['Against']['FG'] + 0.5*data_avg_db[team][max_date]['Against']['3FG'] )/ data_avg_db[team][max_date]['Against']['FGA']
            data_avg_db[team][max_date]['Against']['TOV%'] = data_avg_db[team][max_date]['Against']['TO'] / (data_avg_db[team][max_date]['Against']['FGA'] + 0.44*data_avg_db[team][max_date]['Against']['FTA'] + data_avg_db[team][max_date]['Against']['TO'])
            data_avg_db[team][max_date]['Against']['ORB%'] = data_avg_db[team][max_date]['Against']['ORB'] / (data_avg_db[team][max_date]['For']['DRB'] + data_avg_db[team][max_date]['Against']['ORB'])
            data_avg_db[team][max_date]['Against']['DRB%'] = data_avg_db[team][max_date]['Against']['DRB'] / (data_avg_db[team][max_date]['Against']['DRB'] + data_avg_db[team][max_date]['For']['ORB'])
            data_avg_db[team][max_date]['Against']['FTf'] = data_avg_db[team][max_date]['Against']['FT']/data_avg_db[team][max_date]['Against']['FGA']

            if only_most_recent:
                len_list = 0
            else:
                # Remove the latest date from this list, working backwards to compile totals/averages at each given date
                this_team_idx_list.pop(max_date_idx)
                this_date_list.pop(max_date_idx)
                this_team_home_list.pop(max_date_idx)
                len_list = len(this_team_idx_list)
    return data_avg_db

def save_nn_data(data_avg_db,year):
    # Save Neural Net training data inputs in a pickle file
    pickle_name = 'databases/nn-training-data-inputs-'+year+'.p'         
    with open(pickle_name,'wb') as pick_file:
        pickle.dump(data_avg_db, pick_file)

    print('Saved dictionary: ' + pickle_name)

def main(year):
    
    data_db, conf_teams = load_boxscores(year)
    data_avg_db = create_nn_data(data_db,conf_teams)
    save_nn_data(data_avg_db,year)
    print('Do something.')



if __name__ == '__main__':
    year = input('Year range: ')
    main(year)