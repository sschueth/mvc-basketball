#----------------------------------------------------------------------------
#   money_valley_conference_scraper.py
#   Author: Stephen Schueth
#   Overview: Scrapes the Missouri Valley Conference Men's Basketball
#               website and compiles box scores.
#   Note: This file should only be ran from UTC 1:00 to 6:45 per robots.txt
#   Websites:   http://mvc.org/mbb/stats/2015-16/confstat.htm (example)
#               http://mvc.org/mbb/stats/2015-16/BRAD01.htm (example)
#----------------------------------------------------------------------------

# Import modules
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

# Function to get the links to every game's box score for this year
# Input: Season
# Output: List of links to append to http://mvc.org/mbb/stats/2015-16/______.htm
def get_links_data(year_range):
    
    # Get this seasons schedule home page as html data
    if year_range == '2019-20':
        URL = 'http://mvc.org/mbb/stats/confstat.htm'
    else:
        URL = 'http://mvc.org/mbb/stats/'+year_range+'/confstat.htm'
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    soup_pretty = soup.prettify()
    soup_pretty_list = soup_pretty.split('\n')
    key_link = '<a href'
    ref_list = []
    for idx in range(0,len(soup_pretty_list)):
        if key_link in soup_pretty_list[idx]:
            a_ref = soup_pretty_list[idx]
            a_ref = a_ref.split('"')
            ref_list.append(a_ref[1])

    ind_conf = 'ind-conf.pdf'
    for idx in range(0,len(ref_list)):
        if ind_conf in ref_list[idx]:
            ind_conf_idx = idx
    ref_list_final = ref_list[ind_conf_idx+1:]
    return ref_list_final


# Main fuction to get links of every games box score and save in a .txt file
# Input: N/A
# Output: N/A
def main_get_links():
    mvc_txtfile = 'mvc_game_links_'
    years = ['2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20']
    for idx in tqdm(range(0,len(years))):
        year = years[idx]
        refs = get_links_data(year)
        local_mvc_txtfile = mvc_txtfile + str(idx) + '.txt'
        with open(local_mvc_txtfile,'w') as file:
            for ref in refs:
                file.write('%s\n' % ref)

# Function to scrape the box score from this game in this season
# Input: Season, Game
# Output: Game Title, Box Score as list
def get_game_data(year,game):
    
    # Get this games box score data from the provided url
    if year == '2019-20':
        URL = 'http://www.mvc.org/mbb/stats/'+game
    else:
        URL = 'http://www.mvc.org/mbb/stats/'+year+'/'+game
    r = requests.get(URL)
    soup = BeautifulSoup(r.content,'html5lib')
    soup_pretty = soup.prettify()
    soup_pretty_list = soup_pretty.split('\n')
    title = soup_pretty_list[3]
    
    # Create the games title from the box score title
    title = title.lstrip() + '.txt'
    
    # Find where the box score actually lives in the html
    box_score_start = 0
    box_score_stop = 0
    for i in range(0,len(soup_pretty_list)):
        if '<pre>' in soup_pretty_list[i]:
            box_score_start = i
        if '</pre>' in soup_pretty_list[i]:
            box_score_stop = i
    box_score_list =[]
    
    # Get all the data in the box score
    for i in range(0, len(soup_pretty_list)):
        if i > box_score_start and i < box_score_stop:
            box_score_list.append(soup_pretty_list[i])
            
    # Clean up
    empty_string = ''
    while empty_string in box_score_list:
        box_score_list.remove(empty_string)

    return title, box_score_list

# Main function to get the box scores from all the games in all the seasons
def main_get_games():
    
    # Get links to the games box score
    links_list = []
    with open('mvc_links/mvc_game_links_7.txt','r') as links_file:
        for link in links_file:
            link = link.replace('\n','')
            links_list.append(link)
    
    # Get box score for each link
    for link_idx in tqdm(range(0,len(links_list))):
        tic = time.time()
        file_name, box_score = get_game_data('2019-20',links_list[link_idx])
        # Save box score data as a .txt file
        with open(file_name, 'w') as file:
            for b in box_score:
                file.writelines('%s\n' % b)
        toc = time.time()
        diff = 5 - (toc - tic)
        # robots.txt asks that the crawler-time is at least 5 seconds (don't want to spam their site)
        if diff > 0:
            time.sleep(diff)

if __name__ =='__main__':
    # Pick which "main()" function to run
    resp = input('Do you want to [get links] or [get games]? ')
    if 'get links' in resp:
        print('\nGetting links...\n')
        main_get_links()
    elif 'get games' in resp:
        print ('Getting games...\n')
        main_get_games()
    else:
        print('Price is wrong, b****! - Adam Sandler to Bob Barker')
