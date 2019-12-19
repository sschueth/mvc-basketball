import numpy as np 
import pandas as pd 

with open('Box Score example.txt','r') as myFile:
    data = myFile.readlines()

print(data)

totals_idx = []
for row in range(0,len(data)):
    if 'Totals..' in data[row]:
        totals_idx.append(row)

empty_string = ''
for row in range(0,len(totals_idx)):
    curr_total = data[totals_idx[row]]
    curr_total = curr_total.split(' ')
    while empty_string in curr_total:
        curr_total.remove(empty_string)
    print(curr_total)

blah = 0