'''
Created on Aug 10, 2015

@author: paul
'''

import sys
from configparser import SafeConfigParser
import pathlib


class readConf():

    def __init__(self,file_name):
#         self.Config = ConfigParser()
#         self.Config.read(file_name)
        home = str(pathlib.Path.home())
        self.confFile=file_name
        self.config={}
        default_values={"JobsFile":f"{home}/.doit","ShowDone":1,"WithoutTask":1}
        self.Config = SafeConfigParser()
        if pathlib.Path(self.confFile).exists() :
            self.Config.read(self.confFile)
            self.config["conf_file_exists"] = True
        else :
            self.config["conf_file_exists"] = False

        section="Options"
        for cur_opt in default_values.keys() :
            try:
                self.config[cur_opt] = self.Config.get(section, cur_opt)
            except:
                print("Exception while read config file. No %s option found! Use default value." % cur_opt)
                self.config[cur_opt] = default_values[cur_opt]
                #sys.exit(1)

    def writeShowDoneConf(self,newShowDone):
        if self.config["conf_file_exists"] :
            self.Config.set("Options","ShowDone",str(newShowDone))
            with open(self.confFile, 'w') as configfile:
                self.Config.write(configfile)

if __name__ == '__main__':
    pass
