#!/usr/bin/python

import pySMART
import time
import argparse
import sqlite3


DB_FILE = "db_smart.db"

def parse_args():
    parser = argparse.ArgumentParser(description = "SMART data monitor and history collection")
    parser.add_argument("devices", nargs="+", help = "list of devices to collect information from (at least one required)")

    args = parser.parse_args()
    return args

def get_raw(attr):
    return None if attr is None else attr.raw_int

def get_smart_attrs(device):
    attrs = {
        "raw_read_error_rate": get_raw(device.attributes[1]),
        "power_on_hours": get_raw(device.attributes[9]),
        "power_cycle_count": get_raw(device.attributes[12]),
        "load_cycle_count": get_raw(device.attributes[193]),
        "temperature_celsius": get_raw(device.attributes[194]),
        "reallocated_event_count": get_raw(device.attributes[196]),
        "offline_uncorrectable": get_raw(device.attributes[198]),
    }

    return attrs

def store_device_db(attrs, con):
    cur = con.cursor()

    data = (
        attrs["serial"],
        attrs["ts"],
        attrs["is_ssd"],
        attrs["raw_read_error_rate"],
        attrs["power_on_hours"],
        attrs["power_cycle_count"],
        attrs["load_cycle_count"],
        attrs["temperature_celsius"],
        attrs["reallocated_event_count"],
        attrs["offline_uncorrectable"],
    )

    cur.execute("INSERT INTO smarthist(serial, ts, is_ssd, raw_read_error_rate, power_on_hours, power_cycle_count, load_cycle_count, temperature_celsius, reallocated_event_count, offline_uncorrectable) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    cur.close()

def get_device_attrs(dev_name):
    dev = pySMART.Device(dev_name)

    if dev.interface is None:
        return None

    attrs = get_smart_attrs(dev)
    attrs["serial"] = dev.serial
    attrs["ts"] = int(time.time())
    attrs["is_ssd"] = dev.is_ssd

    return attrs

def main():
    args = parse_args()

    devices = []

    for dev_name in args.devices:
        attrs = get_device_attrs(dev_name)
        if attrs is None:
            print(f"error reading device {dev_name}, exiting...")
        else:
            devices.append(attrs)

    con = sqlite3.connect(DB_FILE)
    for device in devices:
        if device is None:
            continue

        store_device_db(device, con)
        con.commit()

    con.close()

main()

