# create DB file
sqlite3 -batch db_smart.db < tbl_smart.sql
# query DB 
sqlite3 db_smart.db -table "select id, datetime(ts, 'unixepoch', 'localtime') as dt, serial, is_ssd, raw_read_error_rate as read_err_rate, power_on_hours as pw_hours, power_cycle_count as pwr_cycl, load_cycle_count as load_cycl, temperature_celsius as temp, reallocated_event_count as realloc, offline_uncorrectable as offl_unc from smarthist"
