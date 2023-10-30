import os
import re
import argparse
import time
from datetime import datetime
import sys
from influxdb import InfluxDBClient

# set required InfluxDB parameters
host = "localhost"
port = 8086
user = "admin"
password = "admin"
dbname = "mydb"

# how frequently we will write sensor data to the database
sampling_period = 10

def get_cpu_temperature():
    # return CPU temperature as a character string
    res = os.popen("vcgencmd measure_temp").readline()
    return float(res.replace("temp=", "").replace("'C\n", ""))

def get_ram_info():
    """
    return RAM information (unit=kb) in a list:
        - Index 0: total RAM
        - Index 1: used RAM
        - Index 2: free RAM
    """
    p = os.popen("free")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return line.split()[1:4]

def get_cpu_use():
    """
        return % of CPU used by user as a float
    """
    top_processed = os.popen("top -n 1 -b | awk '/%Cpu\(s\)/ {print $2}'").readline()#.strip()
    print(f"test:{top_processed}")
    return float(top_processed)

def get_disk_space():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return line.split()[1:5]

def get_args():
    """
        parses and returns passed in arguments
    """
    parser = argparse.ArgumentParser(description="Program writes measurements data to specified influx db.")

    parser.add_argument(
        "-db", "--database", type=str, help="Database name", required=True
    )
    parser.add_argument(
        "-sn", "--session", type=str, help="Session", required=True
    )
    parser.add_argument(
        "-rn", "--run", type=str, help="Run number", required=False, default=datetime.now().strftime("%Y%m%d%H%M")
    )

    args = parser.parse_args()

    dbname = args.database
    run_number = args.run
    session = args.session
    
    return dbname, session, run_number

def get_data_points():
    """
        get the measurement values
    """
    cpu_usage = get_cpu_use()
    cpu_temp = get_cpu_temperature()
    ram_used_raw = float(get_ram_info()[1]) + 64 * 1024 # the video card takes 64 mb
    print(f"ram used raw: {str(ram_used_raw)}")
    ram_used_percent = int((ram_used_raw / float(get_ram_info()[0])) * 100)
    ram_installed = int(float(get_ram_info()[0]) / 1024)

    disk_free_1 = get_disk_space()[2] # SD card
    disk_free = re.sub("[^0-9]", "", disk_free_1)
    disk_free_nmb = int(disk_free)
    disk_total_1 = get_disk_space()[0]
    disk_total = re.sub("[^0-9]", "", disk_total_1)
    timestamp = datetime.utcnow().isoformat()

    # create influxdb datapoints
    datapoints = [
        {
            "measurement": session,
            "tags": {
                "run_number": run_number,
            },
            "time": timestamp,
            "fields": {
                "cpu_usage": cpu_usage,
                "cpu_temp": cpu_temp,
                "ram_used_percent": ram_used_percent,
                "ram_installed": ram_installed,
                "disk_free": disk_free,
                "disk_free_nmb": disk_free_nmb,
                "disk_total": disk_total
            }
        }
    ]
    return datapoints

# match return values from get_arguments()
# and assign to their respective variables
dbname, session, run_number = get_args()
print(f"Session: {session}")
print(f"Run Number: {run_number}")
print(f"DB Name: {dbname}")

# initalize the influxdb client
client = InfluxDBClient(host, port, user, password, dbname)
try:
    for x in range(1, 4):
        # write datapoints to influxdb
        datapoints = get_data_points()
    bResult = client.write_points(datapoints)
    print(f"Write points {datapoints} Bresult: {bResult}")
    
    # wait for next sample
    time.sleep(sampling_period)
# run until keyboard ctrl-c
except KeyboardInterrupt:
    print("Program stopped by keyboard interrupt [CTRL-C] by user.")
