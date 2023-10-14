#This python program consolidates information from adapter task, dispatcher task, and queue summary CSV files, generated from SMF 115 and 116 data loaded into Db2. 

# importing csv module to handle csv files using python
import csv
# importing os module to handle operating system files using python
import os

adapter_task_list = []

#Only look for adapter task files in the current directory python is executing in, add those files to adapter_task_list
#each CSV file is the generated query output from a QM in an environment 
for filename in os.listdir('.'):
    if(filename.endswith("ADAP.csv")):
        adapter_task_list.append(filename)

#initialize counters to keep track of relevant metrics
zero_counter=0
uniqueIds = set()
space_finder=""
task_count=0
#ADAPTER TASK CHECKER
#This section operates under the assumption that if there are frequently 0's in the 'REQUEST_COUNT' for a particular QM's QCTADP adapter task statistics, not all adapter tasks are being used at a given interval captured. 
# read csv files in adapter_task_list
for adap in adapter_task_list:
    with open(adap, 'r') as csvfile:
        reader= csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the headers
        for val in reader: 
            #if adapter task is not busy at an interval, increment zero_counter
            if(int(val[4])==0):
                zero_counter=zero_counter+1
        #if zero_counter for a given QM's csvfile is more than 80 (arbitrary high value), say there is still room
        if(zero_counter > 80):
            space_finder="Unused adapter tasks - Good"
        #if zero_counter is greater than 20 for a given QM's csvfile, the adapter tasks are probably not all being used. This can be further investigated
        if(zero_counter > 20 & zero_counter < 80):
            space_finder="Potentially room for more adapter tasks - Investigate further"
        else:
            space_finder="Add more adapter tasks"
        print(val[1] + " " + val[2] + " : " + space_finder)
        zero_counter=0 # reset variable
        task_count=0   # reset variable

print("__________________________________________")
#DISPATCHER TASK CHECKER
#This section operates under the assumption that if there are frequently 0's in the 'REQUEST_COUNT' for a particular QM's QCTDSP dispatcher task statistics, not all dispatcher tasks are being used at a given interval captured. 
# read csv files in dispatcher_list
dispatcher_task_list = []

for d_filename in os.listdir('.'):
    if(d_filename.endswith("DISP.csv")):
        dispatcher_task_list.append(d_filename)

d_zero_counter=0
uniqueIds = set()
space_tracker=""

for disp in dispatcher_task_list:
    with open(disp, 'r') as d_csvfile:
        d_reader= csv.reader(d_csvfile, delimiter=',')
        next(d_reader, None)  # skip the headers
        for val in d_reader:
            if(int(val[4])==0):
                d_zero_counter=d_zero_counter+1
        if(d_zero_counter == 0): #if there are no zeros in a given 'REQUEST_COUNT' columnm, the dispatcher task is either 1) overutilized 2) the workload is spread well across
            space_tracker="Distribution even"
        else: #if there are zeros in the 'REQUEST COUNT', there may be skewing towards just a few dispatcher tasks, meaning channels are only using a few dispatcher tasks of those available
            space_tracker="Distribution skewed"
        print(val[1] + " " + val[2] + " : " + space_tracker)
        d_zero_counter=0

print("__________________________________________")
#QUEUE SUMMARY CHECKER
#This section checks queue summary data to pull out all queues with high volumes of skipped messages. 
#read csv files in queue summary
q_list = []

for q_filename in os.listdir('.'):
    if(q_filename.endswith("QSUMMARY.csv")):
        q_list.append(q_filename)

skip_counter=0 #track skip counter for high-skip queues on a particular QM
uniqueIds = set()
high_skip_queues=[] # array of queues that have a high volume of skips
associated_qm=[] # array of queue managers for each queue w/ skips
skip_val=[] # array of skipped message counts

for q in q_list:
    with open(q, 'r') as q_csvfile:
        q_reader= csv.reader(q_csvfile, delimiter=',')
        next(q_reader, None)  # skip the headers
        for val in q_reader:
            if(int(val[16])>0):
                skip_counter=skip_counter+1 
                high_skip_queues.append(str(val[0]).strip())
                associated_qm.append(str(q)[:9])
                skip_val.append(str(val[16]).strip())
        skip_counter=0

for i in range(len(high_skip_queues)):
    #print out all queues with skip counts
    print(high_skip_queues[i] + " Associated QM: " + associated_qm[i] + " Skipped Messages: " + skip_val[i])
    
