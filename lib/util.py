import time
import argparse
import pytz
import dateutil.parser
import logging
from lib.configure import getAllSections

def datetimeToEpoch(dateInDatetime):
    return time.mktime(dateInDatetime.timetuple())


def getUTCTimeDelta():
    return datetime.now(pytz.timezone('US/Pacific')).utcoffset()

def convertTime(time):
    return datetimeToEpoch(datetime.strptime(time, '%m/%d/%Y %H:%M:%S %p'))

def UTCtoPST(time):
    time_out =convertTime(time)
    return str (epochToDatetime(time_out) - getUTCTimeDelta())


def timeDelta(timeDate):
     strDate =  dateutil.parser.parse(timeDate)
     date = strDate.strftime('%m/%d/%Y %H:%M:%S %p')
     print date
     dateFormat  = datetime.strptime(date,'%m/%d/%Y %H:%M:%S %p')
     dateFormat.strftime('%m/%d/%Y %H:%M:%S %p')
     dateWithDelta  = dateFormat + getUTCTimeDelta()
     return str(dateWithDelta.strftime('%m/%d/%Y %H:%M:%S %p'))
def menu(filepath):
    parser = argparse.ArgumentParser(description='Updates and pulls Archer into Splunk')
    parser.add_argument("-s" ,"--source", choices=[option.strip() for option in getAllSections(filepath)])
    return parser

def create_logger(name):
    logger = logging.getLogger(name)
    fmt = logging.Formatter('%(asctime)s - %(name)s -' ' %(levelname)s -%(message)s')
    hdl = logging.FileHandler(name+'.log')
    hdl.setFormatter(fmt)
    logger.addHandler(hdl)

    return logger

def dict_merge(dct, merge_dct):
    for k, v in merge_dct.iteritems():
        if (k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]
def assetType(assetList):
    pass

def healthCheck(source,org,assetList):
    org_count  = 0
    health_count = 0
    server_count = 0
    desktop_count = 0
    other_count = 0
    ips  = [x['ip'] for x in assetList[source] if 'ip' in x]
    for assets in assetList['all_assets']:
        if org in assets['org']: 
           org_count +=1
           if 'True' in assets['server']:
               server_count +=1
           if 'True' in assets['desktop']:
               desktop_count +=1
           if 'True' in assets['other']:
               other_count +=1
        if assets['ip'] in ips:
           if org in assets['org']:
               health_count  +=1
    try:
        percentage = float(health_count)/float(org_count) * int(100)
        return { 'health_count' : health_count , 'org' : org  , 'org_count' : org_count, 'percent' : percentage, 'agent' : source.split('_')[0], 'server_count' : server_count,'desktop_count': desktop_count,'other_count' : other_count}
    except:
        pass
