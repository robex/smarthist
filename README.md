## Save SMART HDD attribute history into a sqlite3 DB
This program was written in order to more easily store and monitor certain SMART attributes (temperature, load cycle count, power cycle count and so on) over time. It was written mostly for mechanical drives, many attributes relevant to SSD or NVMe drives are not saved.

### Usage

Initialize DB:

`sqlite3 -batch db_smart.db < tbl_smart.sql`

Install pySMART (**make sure** the package is available when you run python as **root**):

`pip install pySMART`

Run the program periodically (in cron, systemd, however you want). Example to capture disk data from `/dev/sda`:

`python3 smarthist.py /dev/sda`

Example to capture disk data from `/dev/sda` to `/dev/sdl` (this uses bash expansions):

`python3 smarthist.py /dev/sd[a-l]`


Example to capture disk data from **only** `/dev/sda` and `/dev/sdc`:

`python3 smarthist.py /dev/sda /dev/sdc`

**Running as root** is necessary to query disk attributes, if you know what you're doing you can assign proper permissions/capabilities to any other user instead.

Example query to see results in table format, but you can use these results as you like, or feed them into other tools:

```
sqlite3 db_smart.db -table "select id, datetime(ts, 'unixepoch', 'localtime') as dt, serial, is_ssd, raw_read_error_rate as read_err_rate, power_on_hours as pw_hours, power_cycle_count as pwr_cycl, load_cycle_count as load_cycl, temperature_celsius as temp, reallocated_event_count as realloc, offline_uncorrectable as offl_unc from smarthist"
```

---

### Program help
```
usage: smarthist.py [-h] devices [devices ...]

SMART data monitor and history collection

positional arguments:
  devices     list of devices to collect information from (at least one required)

optional arguments:
  -h, --help  show this help message and exit

```
