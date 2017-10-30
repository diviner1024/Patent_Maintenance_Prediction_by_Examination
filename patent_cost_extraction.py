# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 09:59:14 2017

@author: Zhongyang
This script extracts the data from various USPTO data archives, see the txt file in the folder for urls
"""

import csv
import sys
import cPickle as cP
import json

def extractFromApplication(year):
    iss_date_list = []
    file_date_list = []
    patent_id_list = []
    app_id_list = []
    with open("application_data_2014.csv","r") as f:
        csv_reader = csv.reader(f)
        header = csv_reader.next()
        print zip(header,range(0,len(header)))
        sys.stdout.flush()
        k=0
        for line in csv_reader:
            k+=1
            if k%100000==0:
                print "Processing application file %d"%k
            if k<2000000:
                continue
            iss_date = line[22]
            if line[24]=="ISS" and line[2]=="UTL" and line[3]=="REGULAR":
                if iss_date[0:4]=="2005":
                    app_id_list.append(line[0])
                    patent_id_list.append(line[21])
                    file_date_list.append(line[1].replace("-",""))
                    iss_date_list.append(line[22].replace("-",""))            
    return app_id_list,patent_id_list,file_date_list,iss_date_list
    
def extractFromContinuationTransaction(app_set):
    continue_data = {}
    transaction_data = {}
    for app_id in app_set:
        continue_data[app_id]=[[0,0,0,0],[0,0,0],[-1,-1,0,0],[0,0,0,1]]
        transaction_data[app_id]=[]
    with open("continuity_parents.csv","r") as f:
        csv_reader = csv.reader(f)
        header = csv_reader.next()
        print zip(header,range(0,len(header)))
        sys.stdout.flush()
        k=0
        for line in csv_reader:
            app_id = line[0]
            parent_id = line[1]
            if app_id in continue_data:
                con_status = line[-1]
                if con_status=="DIV" or con_status=="CON" or con_status=="CIP":
                    status_index = 1
                if con_status=="NST":
                    status_index = 0
                if con_status=="PRO":
                    status_index = 3
                continue_data[app_id][0][status_index]+=1
            if parent_id in app_set:
                if con_status=="DIV" or con_status=="CON" or con_status=="CIP":
#                    print continue_data[parent_id]
                    continue_data[parent_id][0][2]+=1            
            k+=1
            if k%200000==0:
                print "Processing continuation file %d"%k
                sys.stdout.flush()
    re_extention_of_time = {"RXXT/G","XT/G","APXG","DT/G"}
#    re_priority_examination = {}
    re_continued_examination = {"RCEX"}
    re_appeal = {"RXN/AP","N/AP"}
    
    with open("transactions.csv","r") as f:
        csv_reader = csv.reader(f,)
        header = csv_reader.next()
        print zip(header,range(0,len(header)))
        sys.stdout.flush()
        k=0
        for line in csv_reader:
            app_id = line[0]
            if app_id in continue_data:
                event_code = line[1]
                if event_code in re_extention_of_time:
                    continue_data[app_id][1][0]+=1
                if event_code in re_continued_examination:
                    continue_data[app_id][1][1]+=1
                if event_code in re_appeal:
                    continue_data[app_id][1][2]+=1                
                transaction_data[app_id].append(event_code)
            k+=1
            if k%1000000==0:
                print "Processing transaction file %d"%k
                sys.stdout.flush()
    with open("pgpub_document_stats.csv","r") as f:
        csv_reader = csv.reader(f)
        header = csv_reader.next()
        print zip(header,range(0,len(header)))
        sys.stdout.flush()
        k=0
        for line in csv_reader:
            app_id = line[1]            
            if app_id in continue_data:
                continue_data[app_id][2][0]=int(line[2])
                continue_data[app_id][2][1]=int(line[5])
            k+=1
            if k%200000==0:
                print "Processing publication claim file %d"%k
    with open("patent_document_stats.csv","r") as f:
        csv_reader = csv.reader(f)
        header = csv_reader.next()
        print zip(header,range(0,len(header)))
        sys.stdout.flush()
        k=0
        for line in csv_reader:
            app_id = line[9]            
            if app_id in continue_data:
                continue_data[app_id][2][2]=int(line[1])
                continue_data[app_id][2][3]=int(line[4])
            k+=1
            if k%200000==0:
                print "Processing patent claim file %d"%k
                sys.stdout.flush()
    large_4 = {"F170 ","F173 ","M1551","M1554","M170 ","M173 ","M183 "}
    large_8 = {"F171 ","F174 ","M1552","M1555","M171 ","M174 ","M181 ","M184 "}
    large_12 = {"F172 ","F175 ","M1553","M1556","M172 ","M175 ","M182 ","M185 "}
    small_4 = {"F273 ","M2551","M2554","M273 ","M283 "}
    small_8 = {"F274 ","M2552","M2555","M274 ","M284 "}
    small_12 = {"F275 ","M2553","M2556","M275 ","M285 "}
    micro_4 = {"M3551","M3554"}
    micro_8 = {"M3552","M3555"}
    micro_12 = {"M3553","M3556"}
    entity = {"N":1,"Y":2,"M":4}
    with open("MaintFeeEvents_20171023.txt","r") as f:
        k=0
        for line in f:
            app_id = line[8:16]            
            if app_id in continue_data:
                continue_data[app_id][3][3] = entity[line[17]]
                event_code = line[46:51]
                if event_code in (large_4 | small_4 | micro_4):
                    continue_data[app_id][3][0] = 1
                if event_code in (large_8 | small_8 | micro_8):
                    continue_data[app_id][3][1] = 1
                if event_code in (large_12 | small_12 | micro_12):
                    continue_data[app_id][3][2] = 1
            k+=1
            if k%200000==0:
                print "Processing maintanence fee file %d"%k
                sys.stdout.flush()
    return continue_data,transaction_data
    
def write_csv(app_id_list,patent_id_list,file_date_list,iss_date_list,continue_data):
    with open("patent_cost_model.csv","w") as f:
        csv_writer = csv.writer(f)
        header = '''App_id,Pat_id,App_date,Iss_date,PCT,Con_Parent,Con_child,Provison,RET,RCE,Appeal,
                    pg_indep_clm,pg_dep_clm,pat_indep_clm,pat_dep_clm,renew_4,renew_8,renew_12,small_entity'''
        csv_writer.writerow(header.split(","))
        for app_id,pat_id,file_date,iss_date in zip(app_id_list,patent_id_list,file_date_list,iss_date_list):
            row_data = [app_id,pat_id,file_date,iss_date]+continue_data[app_id][0]+continue_data[app_id][1]+continue_data[app_id][2]+continue_data[app_id][3]
            csv_writer.writerow(row_data)
    
if __name__ == "__main__":
    app_id_list,patent_id_list,file_date_list,iss_date_list = extractFromApplication(2005)
    cost_data = {"app_id_list":app_id_list,"pat_id_list":patent_id_list,"file_date":file_date_list,"iss_date":iss_date_list}
    json.dump(cost_data,open("patent_cost_1.dat","w"),indent =4)
    continue_data,transaction_data = extractFromContinuationTransaction(set(app_id_list))
    cost_data = {"app_id_list":app_id_list,"pat_id_list":patent_id_list,"file_date":file_date_list,"iss_date":iss_date_list,"continue_data":continue_data}
    cP.dump(cost_data,open("patent_cost.dat","wb"))
    json.dump(transaction_data,open("transaction_data.json","w"),indent = 4)
    write_csv(app_id_list,patent_id_list,file_date_list,iss_date_list,continue_data)
    
