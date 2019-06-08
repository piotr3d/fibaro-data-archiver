import configparser
import os
import helper
from datetime import datetime


if not os.path.isfile('config.ini'):
    with open('config.ini', "w") as myfile:
        myfile.write('# fibaro data archiver config file\n\n')
        myfile.write('[DEFAULT]\n')
        myfile.write('# change fibaro connection settings to match your HC2 IP, user and password\n')
        myfile.write('fibaro_url = http://192.168.81.1/api/\n')
        myfile.write('fibaro_user = user@name.com\n')
        myfile.write('fibaro_password = password\n')
        myfile.write('# location for data files and log, by default subdirectories in the same location as script\n')
        myfile.write('data_directory = data\n')
        myfile.write('log_directory = logs\n')

cfg = configparser.ConfigParser()
cfg.read('config.ini')
fibaro_url = cfg['DEFAULT']['fibaro_url']
fibaro_user = cfg['DEFAULT']['fibaro_user']
fibaro_password = cfg['DEFAULT']['fibaro_password']
data_directory = cfg['DEFAULT']['data_directory']
log_directory = cfg['DEFAULT']['log_directory']
data_backup_directory = os.path.join(data_directory, "bak")
log_file = os.path.join(log_directory, "log_" + datetime.now().strftime('%Y-%m') + ".txt")

# create directories if needed
helper.create_dir_if_not_exists(data_directory)
helper.create_dir_if_not_exists(log_directory)
helper.create_dir_if_not_exists(data_backup_directory)
