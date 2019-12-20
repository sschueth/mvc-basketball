import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

def get_links_data(year_range):

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
            #link_idx_list.append(idx)

    ind_conf = 'ind-conf.pdf'

    for idx in range(0,len(ref_list)):
        if ind_conf in ref_list[idx]:
            ind_conf_idx = idx
    
    ref_list_final = ref_list[ind_conf_idx+1:]

    #print(ref_list_final)
    #print('Scraped: ' + URL)
    return ref_list_final

def main_get_links():
    mvc_txtfile = 'mvc_game_links_'
    years = ['2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19']
    for idx in tqdm(range(0,len(years))):
        year = years[idx]
        refs = get_links_data(year)
        local_mvc_txtfile = mvc_txtfile + str(idx) + '.txt'
        with open(local_mvc_txtfile,'w') as file:
            for ref in refs:
                file.write('%s\n' % ref)

def get_game_data(year,game):
    URL = 'http://www.mvc.org/mbb/stats/'+year+'/'+game
    r = requests.get(URL)
    soup = BeautifulSoup(r.content,'html5lib')
    soup_pretty = soup.prettify()
    soup_pretty_list = soup_pretty.split('\n')
    title = soup_pretty_list[3]
    title = title.lstrip() + '.txt'
    #print(soup_pretty)
    box_score_start = 0
    box_score_stop = 0
    for i in range(0,len(soup_pretty_list)):
        if '<pre>' in soup_pretty_list[i]:
            box_score_start = i
        if '</pre>' in soup_pretty_list[i]:
            box_score_stop = i
    box_score_list =[]
    for i in range(0, len(soup_pretty_list)):
        if i > box_score_start and i < box_score_stop:
            box_score_list.append(soup_pretty_list[i])
    empty_string = ''
    while empty_string in box_score_list:
        box_score_list.remove(empty_string)
    #print('File: '+title)
    #print(box_score_list)
    return title, box_score_list

def main_get_games():
    links_list = []
    with open('mvc_game_links_2.txt','r') as links_file:
        for link in links_file:
            link = link.replace('\n','')
            links_list.append(link)
    for link_idx in tqdm(range(0,len(links_list))):
        tic = time.time()
        file_name, box_score = get_game_data('2014-15',links_list[link_idx])
        with open(file_name, 'w') as file:
            for b in box_score:
                file.writelines('%s\n' % b)
        toc = time.time()
        diff = 5 - (toc - tic)
        if diff > 0:
            time.sleep(diff)

if __name__ =='__main__':
    resp = input('Do you want to [get links] or [get games]? ')
    if 'get links' in resp:
        print('\nGetting links...\n')
        main_get_links()
    elif 'get games' in resp:
        print ('Getting games...\n')
        main_get_games()
    else:
        print('Price is wrong, bitch!!')