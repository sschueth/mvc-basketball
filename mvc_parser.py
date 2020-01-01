#---------------------------------------------------------------------
#   money_valley_conference_parser.py
#   Author: Stephen Schueth
#   Description: Code to filter through all the box scores and parse
#   out the important information and save them in a database
#---------------------------------------------------------------------

# Import Modules
import numpy as np 
import pandas as pd 
import pickle
import os
from tqdm import tqdm

# Function to pull out the import box score statistics from every conference game
# Input: Season i.e. '2015-16'
# Output: Dictionary with box scores for every conference game
def parse_boxscores(year):
    
    # Get all the game .txt files for this season
    files = os.listdir(year)
    
    # Get all the conference teams for this season
    conf_file = year + '/conference teams.txt'
    with open(conf_file,'r') as myFile:
        conf_teams = myFile.readlines()

    conference_teams = []
    for t in conf_teams:
        if '\n' in t:
            t = t.split('\n')
            t = t[0]
        conference_teams.append(t)
    
    # Box Score fields
    team_box_score_order = ['Team Name','FG','FGA','3FG','3FGA','FT','FTA','ORB','DRB','REB','PF','TP','A','TO','BLK','S']
    
    # Initialize dictionary
    game_id = 0
    game_dict = {}
    
    # Iterate through all the games in the season
    for idx in tqdm(range(0,len(files))):
        
        # Parse out the names of the teams in this game
        file_name_txt = files[idx]        
        if 'conference' in file_name_txt or 'Conference' in file_name_txt:
            visitor_team = 'blah'
            home_team = 'blah'
            totals_idx = []
            data = []
        else:
            file_name = file_name_txt[:-4]
            file_date = file_name.split('(')[-1].split(')')[0]
            file_date = file_date.split('-')
            file_month = file_date[0]
            file_day = file_date[1]
            file_year = '20'+file_date[2]
            # Read box score data
            with open(year+'/'+file_name_txt,'r') as myFile:
                data = myFile.readlines()
            # Initialize List
            visitor_team = []
            home_team = []
            totals_idx = []
        
        # Parse out the team names in the box score
        for row in range(0,len(data)):
            if 'Totals..' in data[row]:
                totals_idx.append(row)
            if 'VISITORS:' in data[row]:
                visitor_team = data[row]
                visitor_team = visitor_team.split(':')[1]
                visitor_team = visitor_team.split('(')[0]
                visitor_team = visitor_team.rstrip()
                while visitor_team[0].isalpha() == False:
                    visitor_team = visitor_team[1:]
            if 'HOME TEAM:' in data[row]:
                home_team = data[row]
                home_team = home_team.split(':')[1]
                home_team = home_team.split('(')[0]
                home_team = home_team.rstrip()
                while home_team[0].isalpha() == False:
                    home_team = home_team[1:]

        # Make sure this is a conference game
        num_conf_teams = 0
        for t in conference_teams:
            if t in home_team:
                num_conf_teams = num_conf_teams + 1
            if t in visitor_team:
                num_conf_teams = num_conf_teams + 1

        if num_conf_teams == 2:
            # Initialize dictionary for this game
            game_dict[game_id] = {}
            game_dict[game_id]['Day'] = file_day
            game_dict[game_id]['Month'] = file_month
            game_dict[game_id]['Year'] = file_year
            game_dict[game_id]['Home'] = {}
            game_dict[game_id]['Visitor'] = {}
            game_dict[game_id]['Home']['Team']=home_team
            game_dict[game_id]['Visitor']['Team'] = visitor_team
            
            # Iterate through box score statistics and save them in the appropriate fields in the dict/database
            empty_string = ''
            for row in range(0,len(totals_idx)):
                if row == 0:
                    vis_total = data[totals_idx[row]]
                    vis_total = vis_total.split(' ')
                    while empty_string in vis_total:
                        vis_total.remove(empty_string)
                    vis_total = vis_total[1:-1]
                    for vis_idx in range(0,len(vis_total)):
                        game_dict[game_id]['Visitor'][team_box_score_order[vis_idx+1]] = float(vis_total[vis_idx])
                if row == 1:
                    home_total = data[totals_idx[row]]
                    home_total = home_total.split(' ')
                    while empty_string in home_total:
                        home_total.remove(empty_string)
                    home_total = home_total[1:-1]
                    for home_idx in range(0,len(home_total)):
                        game_dict[game_id]['Home'][team_box_score_order[home_idx+1]] = float(home_total[home_idx])
            
            # Add outcomes for betting purposes: Spread, Moneyline (kind of), and O/U
            game_dict[game_id]['Home +/-'] = game_dict[game_id]['Home']['TP'] - game_dict[game_id]['Visitor']['TP']
            if game_dict[game_id]['Home +/-'] > 0:
                game_dict[game_id]['Home W/L'] = 1
            else:
                game_dict[game_id]['Home W/L'] = 0
            game_dict[game_id]['Total O/U'] = game_dict[game_id]['Home']['TP'] + game_dict[game_id]['Visitor']['TP']
            game_id = game_id + 1
            
    return game_dict

def main():
    years = ['2015-16','2016-17','2017-18','2018-19','2019-20']
    #years = ['2019-20']
    for y in years:
        game_dict = parse_boxscores(year = y)
        
        # Save dict/database as a pickle file
        pickle_name = 'box-score-dict-'+y+'.p'
        with open(pickle_name,'wb') as pick_file:
            pickle.dump(game_dict, pick_file)
            
        print('Saved dictionary: ' + pickle_name)

if __name__ == '__main__':
    main()
