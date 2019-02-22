import json
from util import healthCheck

class AssetDiscovery(object):
    def __init__(self,configs):
        self.configs = configs
        self.tracked = False
        self.SOURCES  = []
        self.getScripts()

    def printConfigs(self):
       print  [[x for x in self.config['sources'].keys] for x,y in self.config['source']]

    def getScripts(self):
        self.SOURCES = [x for x,y  in self.configs['sources'].items() if 'execute' in y and 'True' in y['execute']]
    
    def printSource(self):
         print self.SOURCES

    def getScriptEXE(self):
        self.scriptDict = {}
        for source in self.SOURCES:
            localPath = "sources.%s" % (source)
            try:
                self.scriptDict[source] = __import__(localPath,fromlist=['excute'])
            except(ImportError) as e:
                print "Import Error %s" % (e)

        return self.scriptDict

    def mergeRecords(self,results):
         finalRecord =  collections.defaultdict(set)
         for record in results:
             for (k,v) in record.iteritems():
                 finalRecord[k].add(v)
         return  finalRecord

class AssetAttr():
    def __init__(self,configs):
        self.configs = configs
    def getKVstores(self):
        return [ y['kvstore']  for x,y in self.configs['sources'].items() if 'store' in y and 'True' in y['store']] 

    def getKVstore(self,name):
        return [ self.configs['sources'][name]['kvstore']]

    def getAgents(self):
        return [y['kvstore'] for x,y in self.configs['sources'].items() if 'health' in y and 'True' in y['health']]

class AssetQuery():
    def getKVinfo(self,kv,splunk):
        allKV = {}
        for store in kv:
            try:
               allKV[store] = splunk.getKVstore(store)
            except Exception as e:
                print 'This is the error %s' %  (e)
        return allKV
class AssetHealthCheck():

      def __init__(self,**kwargs):

           self.update    = kwargs['update'] 
           self.source    = kwargs['source'] 
           self.assetList = kwargs['assetList']
      
      def getHealthIPs(assetDict):
          return list(set(record['ip'] for record in assetDict[agent] if 'ip' in record))

      @classmethod
      def healthCheck(cls,agent,org,assetDict):
           agentIPs  = list(set(record['ip'] for record in assetDict[agent] if 'ip' in record))
           orgCount,healthCount,serverCount,desktopCount,other_count,unhealthyTotal = (0,0,0,0,0,0)

           for assets in assetDict['all_assets']:
               if org in assets['org'] and assets['ip'] in agentIPs:
                   orgCount +=1
                   healthCount  +=1
                   if 'True' in assets['server']:
                       serverCount +=1
                   if 'True' in assets['desktop']:
                       desktopCount +=1
                   if 'True' in assets['other']:
                       other_count +=1
               else:
                   unhealthyTotal +=1
           try:
                percentage  = 0
                return { 'health_count' : healthCount , 'org' : org  , 'org_count' : orgCount, 'percent' : percentage, 'agent' : agent.split('_')[0], 'server_count' : serverCount,'desktop_count': desktopCount,'other_count' : other_count}
           except Exception as e:
                  print e
class AssetStore():
     def __init__(self,agent,groups,kvinfo,splunk):
         self.agent = agent
         self.groups = groups
         self.kvinfo = kvinfo
         self.splunk = splunk

     def storeKVinfo(self):
         for group in self.groups:
             data = json.dumps(AssetHealthCheck.healthCheck(self.agent,group,self.kvinfo))
             if 'null' not in data:
                 self.splunk.setKVstore('health_assets',data)  #fix
