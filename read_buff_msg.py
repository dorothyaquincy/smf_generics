#This python program consolidates information from adapter task, dispatcher task, and queue summary CSV files, generated from SMF 115 and 116 data loaded into Db2. 

# importing csv module to handle csv files using python
import csv
# importing os module to handle operating system files using python
import os
import pandas as pd


bp_list = []
mm_list = []

for filename in os.listdir('.'):
    if(filename.endswith("BuffMgr.csv")):
        bp_list.append(filename)
    if(filename.endswith("MSGMgr.csv")):
        mm_list.append(filename)

for i in range(len(bp_list)):
    df=pd.read_csv(bp_list[i])
    #FINDING MAX AND MIN
    p=df['Highest Used Percent'].max()*100
    q=df['DASD Write'].max()
    r=df['Defer Write Thold Reached'].max()
    print(bp_list[i] + " highest used percent: " + str(p) + " DASD Writes: " + str(q) + " DWT Reached " + str(r))



for i in range(len(mm_list)):
    df=pd.read_csv(mm_list[i])
    #FINDING MAX AND MIN
    p=df['Put'].max()
    q=df['Put'].min()
    r=df['Get'].max()
    s=df['Get'].min()

    if(p>500000):
       print(mm_list[i] + " Put Max: " + str(p) + " Put Min: " + str(q) + " Get Max: " + str(r) + " Get Min: " + str(s))


