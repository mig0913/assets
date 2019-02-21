import  ConfigParser, os, logging, getpass, sys
from collections import OrderedDict
from copy import deepcopy


def getConfigFiles(confBasePath):

    configs = OrderedDict()
    confs = OrderedDict()
    
    for base,dirs,files in sorted([x for x in os.walk(confBasePath)]):
        for filename in sorted([x for x in files if x.endswith(".conf")]):
    	    if filename not in confs:
    	        confs[filename] = []
    	    confs[filename].append(os.path.join(base,filename))
    for confName,confPaths in confs.iteritems():
        conf = populateConfig(confPaths)
        configs[confName.split('.conf')[0]] = conf

    return configs

def populateConfig(confPaths):
    config = OrderedDict()
    default = OrderedDict()

    def getConfig(config,parsers):   
        for parser in parsers:
            for section in parser.sections():
                if section not in config:
                    config[section] = deepcopy(default)
                for opt,val in parser.items(section):
                    config[section][opt] = val
    parsers = []
    for confPath in confPaths:
        parsers.append(ConfigParser.ConfigParser())
        parsers[-1].optionxform = str
        parsers[-1].read(confPath)

    getConfig(config,parsers)
    return config

def getSources(source):
    try:
        config = ConfigParser.RawConfigParser()
        config.readfp(open(source))
        return config.sections()
    except (ConfigParser.Error):
        return

def getData(filename,section,item):
	config = ConfigParser.ConfigParser()
	config.read(filename)
        try:
           if 'splunk' in section:
               return config.get(section,item) #Fix
           elif 'True' in config.get(section,item): return config.get(section,item)
        except:
           return
         
def getAllSections(filepath):
    config = ConfigParser.ConfigParser()
    config.read(filepath)        
    return config.sections()
