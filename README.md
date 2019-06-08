# fibaro-data-archiver

This is a simple script that retrieves and stores data from Fibaro HC2 (Z-wave controller). Due to the limited storage Fibaro purges old data and I wanted to keep them longer. In my case event data was lost after 7-8 days which was the main reason to come up with a way to archive it.

* *main.py* - this is the main script (run this one)<br/>
* *config.py* - get configuration data from *config.ini* file (creates one if it doesn't exist)
* *helper.py* - internal helper functions
* *requirements* - list of required libraries - requests and it's dependecies

## How I use it
I've put this script on my Synology and created a scheduled task that runs daily and stores the data on NAS.
