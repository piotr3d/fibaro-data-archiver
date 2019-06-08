from datetime import datetime
from datetime import timedelta
import time
import json
import requests
import os
import filecmp
import config


def write_log(line, eol=True, dtm_prefix=True):
    with open(config.log_file, "a") as myfile:
        if dtm_prefix:
            myfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": ")
        myfile.write(line)
        if eol:
            myfile.write("\n")


def write_json(json_data, dest_file_path):
    with open(dest_file_path, 'w') as f:
        json.dump(json_data, f)


def get_fibaro_data_from_api(obj):
    write_log(datetime.now().strftime("### Getting data from " + obj + " API: "), eol=False)
    target_url = config.fibaro_url + obj
    try:
        r = requests.get(target_url, auth=(config.fibaro_user, config.fibaro_password))
    except requests.exceptions.ConnectionError:
        write_log("ERROR: Connection error for " + target_url)
        raise SystemExit("ERROR: Connection error for " + target_url)
    if r.status_code == 200:
        data = r.json()
        filename = os.path.join(config.data_directory, obj + ".json")
        exists = os.path.isfile(filename)
        if exists:
            write_json(data, filename + ".temp")
            filecmp.clear_cache()
            if os.path.getsize(filename) == os.path.getsize(filename + ".temp"):
                os.remove(filename + ".temp")
                write_log("File already existed and is the same. Keeping old file: " + filename, dtm_prefix=False)
            else:  # files are different
                # backup old file
                backup_filename = os.path.join(config.data_backup_directory, obj + ".json") + \
                                  datetime.now().strftime('.%Y-%m-%d-%H-%M-%S.bak')
                os.rename(filename, backup_filename)
                # rename temporary file
                os.rename(filename + ".temp", filename)
                write_log("File already exists but it's different. Old file was backed up as: " +
                          backup_filename, dtm_prefix=False)
        else:
            write_json(data, filename)
            write_log("File downloaded and stored as: " + filename, dtm_prefix=False)
    else:
        write_log("ERROR: error from " + obj + "API code: " + str(r.status_code))


write_log(datetime.now().strftime("##################### New process started"))
get_fibaro_data_from_api("sections")
get_fibaro_data_from_api("rooms")
get_fibaro_data_from_api("scenes")
get_fibaro_data_from_api("devices")

today_bod = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
today_eod = today_bod+timedelta(1)

start_time = time.time()

write_log(datetime.now().strftime("### Getting data from Events API"))

# Events
# Get last 7 days (+ today)
for d in range(8):
    delta = d
    start_dt = today_bod-timedelta(delta)
    end_dt = today_eod-timedelta(delta)
    start = str(int(datetime.timestamp(start_dt)))
    end = str(int(datetime.timestamp(end_dt)))

    target_url = config.fibaro_url + 'panels/event?' + 'from=' + start + "&" + "to=" + end
    try:
        r = requests.get(target_url, auth=(config.fibaro_user, config.fibaro_password))
    except requests.exceptions.ConnectionError:
        write_log("ERROR: Connection error for " + target_url)
        raise SystemExit("ERROR: Connection error for " + target_url)
    if r.status_code == 200:
        data = r.json()
        filename = os.path.join(config.data_directory, start_dt.strftime('events_%Y-%m-%d-%H-%M-%S') +
                                "_-_" + end_dt.strftime('%Y-%m-%d-%H-%M-%S')+".json")
        # event file for this event exists?
        exists = os.path.isfile(filename)
        if exists:
            write_json(data, filename + ".temp")
            filecmp.clear_cache()
            if os.path.getsize(filename) == os.path.getsize(filename + ".temp"):
                os.remove(filename + ".temp")
                write_log("File already existed and is the same. Keeping old file: " + filename)
            else:  # files are different
                # backup old file
                backup_filename = os.path.join(config.data_backup_directory, start_dt.strftime('events_%Y-%m-%d-%H-%M-%S') +
                                               "_-_" + end_dt.strftime('%Y-%m-%d-%H-%M-%S')+".json" +
                                               datetime.now().strftime('.%Y-%m-%d-%H-%M-%S.bak'))
                os.rename(filename, backup_filename)
                # rename temporary file
                os.rename(filename + ".temp", filename)
                write_log("File already exists but it's different. Old file was backed up as: " + backup_filename)
        else:
            write_json(data, filename)
            write_log("File downloaded and stored as: " + filename)

        write_log("Downloaded events from date: " + start_dt.strftime('%Y-%m-%d') + ": " + target_url)
    else:
        write_log("ERROR: error from API code: " + str(r.status_code))
    time.sleep(0.1)

# write_log(datetime.now().strftime("### Getting data from Energy API"))
# ids =
# http://10.0.0.28/api/energy/serialize?from=1528840064&to=1559944064&id=94,87,88,89,90,91,641,435,0&getby=rooms

write_log(datetime.now().strftime("##################### Update process completed"))
