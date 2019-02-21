import os
from lib.configure import getConfigFiles
from lib.asset import AssetDiscovery,AssetAttr
from lib.splunk import Splunk
global configs,final

def launchscripts(source,configs):
    """ Executes all scripts that are enabled = True in sources.conf"""
    for name,module in source.iteritems():
        print "Executing %s" % (name)
        module.execute(configs) #AssetDiscovery.getScriptEXE fromlist=['excute']

#Get current directory of collect.py
script_home = os.path.dirname(os.path.realpath(__file__))
#Get all configuration files in etc dir
configs = getConfigFiles(os.path.join(script_home, 'etc'))

#Look for execute = True in configs
exe  = AssetDiscovery(configs)
configAttr = AssetAttr(configs)
scripts = exe.getScriptEXE()
##Execute all script in source dir where execute =True 
launchscripts(scripts,configAttr)
