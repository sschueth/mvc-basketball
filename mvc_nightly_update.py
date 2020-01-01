# ------------------------------------------------------
# mvc_nightly_update.py
# Author: Stephen Schueth
# Date: 1/1/2020
#
# Description:
# This file is meant to be the master update file, calls
# scraper file, parsing file, new nn data file, re-train
# nns. Ideally, this is the only thing that needs to be 
# ran before predicting the game outcomes.
#-------------------------------------------------------

import numpy as np
import mvc_create_nn_data, mvc_scraper, mvc_parser, mvc_nn_mlp_regression
import time



def main():
    sleep_time = 2
    print('\nScraping mvc.org to get links to the latest box scores....')
    time.sleep(sleep_time)
    mvc_scraper.main_get_links()
    print('\nScraping the latest box scores.')
    time.sleep(sleep_time)
    mvc_scraper.main_get_games()
    print('\nParsing this seasons data.')
    time.sleep(sleep_time)
    mvc_parser.main()
    print('\nFormatting the parsed data into NN I/O.')
    time.sleep(sleep_time)
    mvc_create_nn_data.main(year = '2019-20')
    print('\nCreating NN.')
    time.sleep(sleep_time)
    mvc_nn_mlp_regression.main()
    print('\nReady to go!!')
    time.sleep(sleep_time)

if __name__ == '__main__':
    main()