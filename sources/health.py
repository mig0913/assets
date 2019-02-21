from lib.splunk import Splunk
import itertools
from lib.splunk import Splunkit
import sys
import os
from lib.asset import AssetDiscovery,AssetQuery,AssetHealthCheck
import re
import json
from lib.configure import getConfigFiles,getData,getAllSections,getSources
from lib.util import healthCheck

config_file = '/home/ir/Code/asset/etc/sources.conf'
groups = [
'Call Center',
'Citrix', 
'Costco Travel',  
'ECOM',   
'Facilities',     
'Gasoline',       
'Networking',     
'None',
'Optical',
'Pharmacy',
'Regionals',
'Warehouse']

def execute(configAttr):
    agents = configAttr.getAgents()
    #kv =  configAttr.getKVstores()
    #splunk = Splunkit()
    #query = AssetQuery()
    #kvinfo =  query.getKVinfo(kv,splunk)
    #query.storeKVinfo(agents,groups,kvinfo,splunk)
