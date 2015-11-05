'''
Created on Aug 10, 2015

@author: paul
'''

import sys
from ConfigParser import SafeConfigParser


class readConf():
    
    def __init__(self,file_name):
#         self.Config = ConfigParser()
#         self.Config.read(file_name)
        self.confFile=file_name
        self.config={}
        default_values={"JobsFile":"~/.doit","ShowDone":1,"WithoutTask":1}        
        self.Config = SafeConfigParser()       
        self.Config.read(self.confFile)        
#         print Config.get("Options", "JobsFile")
      
        section="Options"
        for cur_opt in default_values.keys() :
#             print cur_opt
#             print Config.get(section, cur_opt)            
            try:
                self.config[cur_opt] = self.Config.get(section, cur_opt)
            except:
                print("Exception while read config file. No %s option found! Use default value." % cur_opt)
                self.config[cur_opt] = default_values[cur_opt]
                #sys.exit(1)
            
    def writeShowDoneConf(self,newShowDone):
        self.Config.set("Options","ShowDone",str(newShowDone))
        with open(self.confFile, 'wb') as configfile:
            self.Config.write(configfile)       
              

if __name__ == '__main__':
    pass