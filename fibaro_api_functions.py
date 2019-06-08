from datetime import datetime
from datetime import timedelta
import config
import helper as hlp
import os
import requests
import time

def get_data(obj):
    hlp.write_log("### Getting data from " + obj + " API: ", eol=False)
    target_url = config.fibaro_url + obj
    try:
        r = requests.get(target_url, auth=(config.fibaro_user, config.fibaro_password))
    except requests.exceptions.ConnectionError:
        hlp.write_log("ERROR: Connection error for " + target_url)
        raise SystemExit("ERROR: Connection error for " + target_url)
    if r.status_code == 200:
        data = r.json()
        filename = os.path.join(config.data_directory, obj + ".json")
        exists = os.path.isfile(filename)
        if exists:
            hlp.write_json(data, filename + ".temp")
            if os.path.getsize(filename) == os.path.getsize(filename + ".temp"):
                os.remove(filename + ".temp")
                hlp.write_log("File already existed and is the same. Keeping old file: " + filename, dtm_prefix=False)
            else:  # files are different
                # backup old file
                backup_filename = os.path.join(config.data_backup_directory, obj + ".json") + \
                                  datetime.now().strftime('.%Y-%m-%d-%H-%M-%S.bak')
                os.rename(filename, backup_filename)
                # rename temporary file
                os.rename(filename + ".temp", filename)
                hlp.write_log("File already exists but it's different. Old file was backed up as: " +
                              backup_filename, dtm_prefix=False)
        else:
            hlp.write_json(data, filename)
            hlp.write_log("File downloaded and stored as: " + filename, dtm_prefix=False)
    else:
        hlp.write_log("ERROR: error from " + obj + "API code: " + str(r.status_code))


def get_events(days=8):
    today_bod = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_eod = today_bod + timedelta(1)

    hlp.write_log(datetime.now().strftime("### Getting data from Events API"))

    # Events
    # Get last 7 days (+ today)
    for d in range(days):
        delta = d
        start_dt = today_bod - timedelta(delta)
        end_dt = today_eod - timedelta(delta)
        start = str(int(datetime.timestamp(start_dt)))
        end = str(int(datetime.timestamp(end_dt)))

        target_url = config.fibaro_url + 'panels/event?' + 'from=' + start + "&" + "to=" + end
        try:
            r = requests.get(target_url, auth=(config.fibaro_user, config.fibaro_password))
        except requests.exceptions.ConnectionError:
            hlp.write_log("ERROR: Connection error for " + target_url)
            raise SystemExit("ERROR: Connection error for " + target_url)
        if r.status_code == 200:
            data = r.json()
            filename = os.path.join(config.data_directory, start_dt.strftime('events_%Y-%m-%d-%H-%M-%S') +
                                    "_-_" + end_dt.strftime('%Y-%m-%d-%H-%M-%S') + ".json")
            # event file for this event exists?
            exists = os.path.isfile(filename)
            if exists:
                hlp.write_json(data, filename + ".temp")
                if os.path.getsize(filename) == os.path.getsize(filename + ".temp"):
                    os.remove(filename + ".temp")
                    hlp.write_log("File already existed and is the same. Keeping old file: " + filename)
                else:  # files are different
                    # backup old file
                    backup_filename = os.path.join(config.data_backup_directory,
                                                   start_dt.strftime('events_%Y-%m-%d-%H-%M-%S') +
                                                   "_-_" + end_dt.strftime('%Y-%m-%d-%H-%M-%S') + ".json" +
                                                   datetime.now().strftime('.%Y-%m-%d-%H-%M-%S.bak'))
                    os.rename(filename, backup_filename)
                    # rename temporary file
                    os.rename(filename + ".temp", filename)
                    hlp.write_log(
                        "File already exists but it's different. Old file was backed up as: " + backup_filename)
            else:
                hlp.write_json(data, filename)
                hlp.write_log("File downloaded and stored as: " + filename)

            hlp.write_log("Downloaded events from date: " + start_dt.strftime('%Y-%m-%d') + ": " + target_url)
        else:
            hlp.write_log("ERROR: error from API code: " + str(r.status_code))
        time.sleep(0.1)
