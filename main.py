import fibaro_api_functions as api
import helper as hlp

hlp.write_log("##################### New process started")
api.get_data("sections")
api.get_data("rooms")
api.get_data("scenes")
api.get_data("devices")
api.get_events()
hlp.write_log("##################### Update process completed")
