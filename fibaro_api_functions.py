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
    r = call_fibaro_api(target_url)
    if r.status_code == 200:
        save_data(r.json(), obj)
    else:
        hlp.write_log("ERROR: error from " + obj + "API code: " + str(r.status_code))


def get_events(days=8):
    today_bod = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_eod = today_bod + timedelta(1)
    hlp.write_log(datetime.now().strftime("### Getting data from Events API"))
    # Get last n days (including today)
    for d in range(days):
        start_dt = today_bod - timedelta(d)
        end_dt = today_eod - timedelta(d)
        start = str(int(datetime.timestamp(start_dt)))
        end = str(int(datetime.timestamp(end_dt)))

        target_url = config.fibaro_url + 'panels/event?' + 'from=' + start + "&" + "to=" + end
        r = call_fibaro_api(target_url)
        if r.status_code == 200:
            save_data(r.json(), start_dt.strftime('events_%Y-%m-%d-%H-%M-%S') + "_-_"
                      + end_dt.strftime('%Y-%m-%d-%H-%M-%S'))
            hlp.write_log("Downloaded events from date: " + start_dt.strftime('%Y-%m-%d') + ": " + target_url)
        else:
            hlp.write_log("ERROR: error from API code: " + str(r.status_code))
        time.sleep(0.1)


def save_data(json_data, filename_part):
    filename_with_path = os.path.join(config.data_directory, filename_part + ".json")
    temp_filename_with_path = filename_with_path + ".temp"
    bak_filename_with_path = os.path.join(config.data_backup_directory, filename_part + ".json"
                                          + datetime.now().strftime('.%Y-%m-%d-%H-%M-%S.bak'))
    exists = os.path.isfile(filename_with_path)
    if exists:
        hlp.write_json(json_data, temp_filename_with_path)
        if os.path.getsize(filename_with_path) == os.path.getsize(temp_filename_with_path):
            os.remove(temp_filename_with_path)
            hlp.write_log("File already existed and is the same. Keeping old file: "
                          + filename_with_path, dtm_prefix=False)
        else:  # files are different
            # backup old file
            os.rename(filename_with_path, bak_filename_with_path)
            # rename temporary file
            os.rename(temp_filename_with_path, filename_with_path)
            hlp.write_log("File already exists but it's different. Old file was backed up as: " +
                          bak_filename_with_path, dtm_prefix=False)
    else:
        hlp.write_json(json_data, filename_with_path)
        hlp.write_log("File downloaded and stored as: " + filename_with_path, dtm_prefix=False)


def call_fibaro_api(url):
    try:
        response = requests.get(url, auth=(config.fibaro_user, config.fibaro_password))
    except requests.exceptions.ConnectionError:
        hlp.write_log("ERROR: Connection error for " + url)
        raise SystemExit("ERROR: Connection error for " + url)
    return response
