import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

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
    print(soup_pretty)

def main_get_games():
    get_game_data('2017-18','1718GM01.htm')

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