# Plugin to handle the tools capable of setting the input for "AndroWarn" and handle the output
import os
import database as db
import subprocess
import configparser
import logging as log
import datetime

config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

pluginName = "AndroWarn"
enable = False

# Define any specific configuration directives here
androWarnLocation = config['ANDROWARN']['androWarnLocation']

# this one is mandatory -> where to place the results of the tool
jsonResultsLocation = config['SCANNER']['jsonResultsLocation'] + "/" + pluginName + "/"


class PluginClass:
    def __init__(self):
        ''' constructor '''
        
    def run(self, apk_file, md5, package=''):
        print("Running the AndroWarn plugin!...")
        log.debug("Running the AndroWarn plugin!...")
        # test the existence of the results directory
        if not os.path.exists(jsonResultsLocation):
            os.system("mkdir " + jsonResultsLocation)

        print(pluginName + ": FILE -> " + apk_file)
        log.debug(pluginName + ": FILE -> " + apk_file)

        apkPackageName = os.path.basename(apk_file)

        if apk_file[-4:] == ".apk":
            print(pluginName + ": Running on -> " + apk_file)
            log.debug(pluginName + ": Running on -> " + apk_file)
            print(pluginName + ": Executing -> " + config['GENERAL']['python2cmd'] + " " + androWarnLocation + "androwarn.py -i " + apk_file + " -r json -v 3")
            log.debug(pluginName + ": Executing -> " + config['GENERAL']['python2cmd'] + " " + androWarnLocation + "androwarn.py -i " + apk_file + " -r json -v 3")
            # ----- Start Time ------
            startTime = datetime.datetime.now()
            os.system(config['GENERAL']['python2cmd'] + " " + androWarnLocation + "androwarn.py -i " + apk_file + " -r json -v 3")
            # move the json result file to the appropriate location
            print(pluginName + ": mv " + apkPackageName + ".json " + jsonResultsLocation + md5 + ".json")
            log.debug(pluginName + ": mv " + apkPackageName + ".json " + jsonResultsLocation + md5 + ".json")
            os.system("mv " + apkPackageName + ".json " + jsonResultsLocation + md5 + ".json")
            # have also the information registered on the database
            db.insert_results(md5, pluginName, jsonResultsLocation + md5 + ".json", 0, "")

            endTime = datetime.datetime.now()

            dir = './apkTimeAnalysis'
            if not os.path.exists(dir):
                os.system("mkdir " + dir)
            
                       
            data = md5+' '+pluginName+' '+str(endTime-startTime)+'\n'
            
            with open(dir + '.txt', 'a') as f:
                f.write(data)
