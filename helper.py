# Helper functions for fibaro data archiver
import os


def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
