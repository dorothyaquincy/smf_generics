#This python program consolidates information from adapter task, dispatcher task, and queue summary CSV files, generated from SMF 115 and 116 data loaded into Db2. 

# importing csv module to handle csv files using python
import csv
# importing os module to handle operating system files using python
import os
import pandas as pd


bp_list = []
mm_list = []

for filename in os.listdir('.'):
    if(filename.endswith("Type11LongLatch.csv")):
        bp_list.append(filename)
    if(filename.endswith("Over10KLatch.csv")):
        mm_list.append(filename)

# for i in range(len(bp_list)):
#     df=pd.read_csv(bp_list[i])
#     #FINDING MAX AND MIN
#     p=df['Highest Used Percent'].max()*100
#     print(bp_list[i] + " highest used percent: " + str(p) + " DASD Writes: " + str(q) + " DWT Reached " + str(r))



for i in range(len(mm_list)):
    df=pd.read_csv(mm_list[i])
    #FINDING MAX AND MIN
    p=df['Max Latch Wait Type'].value_counts()

    print(mm_list[i] + " Observed latch types: \n" + str(p))


