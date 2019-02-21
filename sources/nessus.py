from lib.splunk import Splunkit
from lib.asset import AssetQuery,AssetHealthCheck,AssetStore
import json

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
    with open('/home/ir/Code/asset/data/nessus.json') as f:
         data = json.load(f)

         for x in data:
             print x
    #Locate which KV store to store
    #kv  =  configAttr.getKVstore('splunkassets') #fix dynamic 
   # kv =  configAttr.getKVstores()
   # #Splunk instance
   # splunk = Splunkit()
   # #AssetQuery instance to query the KV store
   # query = AssetQuery()
   # kvinfo = query.getKVinfo(kv,splunk)
   # #Define agent #Fix
   # agent = 'nessus_assets'
   # check = AssetStore(agent,groups,kvinfo,splunk)
   # check.storeKVinfo()
