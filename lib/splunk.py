import splunklib.client as client
import splunklib.results as results
import logging, socket, random, re
from splunklib.client import AuthenticationError
from lib.configure import getConfigFiles,getData
import json
import os.path as path

#Search Splunk Creds
localPath =  path.dirname(__file__)
confPath  =  path.join(localPath,'../etc/splunk.conf')
print confPath
username = getData(confPath,'splunk','USERNAME')
password = getData(confPath,'splunk','PASSWORD')
host = getData(confPath,'splunk','HOSTNAME')

print username
print password
print host
class Splunk():
    def __init__(self, host=host, port=8089, username=username, password=password, scheme="https"):
        
        self.connected = False

        try:
            self.service = client.connect(host=host, port=port, username=username, password=password, scheme=scheme, autologin=True)
            self.connected = True
        except(socket.error):
            log.error("Error: Unable to connect to Splunk API.")
            log.debug('msg="Unable to connect to Splunk instance" server="%s" port="%s" user="%s"' % (host, port, username))
            return
        self.jobs = self.service.jobs
        self.previousJobs = []
    def search(self, search, searchArgs=None, resultFunc=None, blocking=True):
        global job

        if blocking:
            #kwargs_blockingsearch = {"exec_mode": "blocking", "count": 0}
            kwargs_blockingsearch = {"count": 0}

            #job = self.jobs.create(search, **kwargs_blockingsearch)
            job = self.jobs.oneshot(search, **kwargs_blockingsearch)
        else:
            job = self.jobs.create(search)

        #self.previousJobs.append(job['sid'])            

        #searchResults = results.ResultsReader(job.results())
        searchResults = results.ResultsReader(job)
        #print [x for x in searchResults]        
        if resultFunc:
            for result in searchResults:
                resultFunc(result)
        else:
            #return list(searchResults)
            return searchResults

    def getLatestSID(self):
        return self.previousJobs[-1]

    def getAllSIDs(self):
        return self.previousJobs

class Splunkit():
    def __init__(self, host=host, port=8089, username=username, password=password, scheme="https"):
        self.connected = False

        try:
            self.service = client.connect(host=host, port=port, username=username, password=password, scheme=scheme,app="costco_assets_ir" ,autologin=True)
            self.connected = True
        except(socket.error):
            log.error("Error: Unable to connect to Splunk API.")
            log.debug('msg="Unable to connect to Splunk instance" server="%s" port="%s" user="%s"' % (host, port, username))
            return

    def setKVstore(self,kvstore,data):
        collection = self.service.kvstore[kvstore]
        collection.data.insert(data)

    def getKVstore(self,kvstore):
        collection = self.service.kvstore[kvstore]
        #return json.dumps(collection.data.query(), indent=1)
        return collection.data.query()
