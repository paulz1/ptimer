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
        self.config={}
        default_values={"JobsFile":"~/.doit","ShowDone":1}        
        Config = SafeConfigParser()       
        Config.read(file_name)        
#         print Config.get("Options", "JobsFile")
      
        section="Options"
        for cur_opt in default_values.keys() :
#             print cur_opt
#             print Config.get(section, cur_opt)            
            try:
                self.config[cur_opt] = Config.get(section, cur_opt)
            except:
                print("Exception while read config file. No %s option found! Use default value." % cur_opt)
                #sys.exit(1)        

if __name__ == '__main__':
    pass