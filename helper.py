# Helper functions for fibaro data archiver
from datetime import datetime
import os
import config as cfg
import json


def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def write_log(line, eol=True, dtm_prefix=True):
    with open(cfg.log_file, "a") as myfile:
        if dtm_prefix:
            myfile.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": ")
        myfile.write(line)
        if eol:
            myfile.write("\n")


def write_json(json_data, dest_file_path):
    with open(dest_file_path, 'w') as f:
        json.dump(json_data, f)
