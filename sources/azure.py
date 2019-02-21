from lib.splunk import Splunk
import sys
import re
import csv
import logging
from lib.util import create_logger

def execute():
    logger = create_logger('azure-bro')
    logger.setLevel(logging.INFO)
    
    #Splunk Object
    sp = Splunk ()
    
    #broIP = '''search index=bro_conn earliest_time=-1h
    #| dedup src_ip
    #| rex field=src_ip "(?<ip>^10\.20[8-9]\.\d+\.\d+)"
    #| where ip!=""
    #| table ip'''
    
    # Splunk queries
    
    broIP = '''search index=bro_conn src_ip!="" earliest_time=-24h
    | dedup src_ip
    | table src_ip'''
    
    cmdbQuery = '''search index="servicenow" sourcetype="snow:cmdb_ci_server" earliest=-24h
    | dedup  ip_address
    | table  ip_address '''
    
    broAzure = []
    carts = []
    results = []
    
    try:
    
        broResults  = (sp.search(broIP))
        azureIp = re.compile("(^10\.20[8-9]\.\d+\.\d+)")
       
        for result  in broResults:
            if azureIp.match(result['src_ip']) : broAzure.append(result['src_ip'])
            print result
        broAzure = list(set(broAzure))
        logger.info("Bro => %s unique ips ", len(broAzure))
    except(StopIteration):
        print "No results \n"
    
    try:
        cartsResults  = (sp.search(cmdbQuery))
        for result in cartsResults:
            if 'ip_address' in result: 
                carts.append(result['ip_address'])
        logger.info("Cart => %s unique ips", len(carts))
    except(StopIteration):
        print "No results \n"
    
    [results.append(ip) for ip in broAzure if ip not in carts]
    
    logger.info("%s ips aren't in CARTS", len(results))
    
    
    with open ('azureips.csv','wb') as csvfile:
         ws = csv.writer(csvfile)
         ws.writerow(results)
    
