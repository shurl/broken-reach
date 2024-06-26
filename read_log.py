import argparse
import datetime
import json

parser = argparse.ArgumentParser()
parser.add_argument("--path", help="Parse log at the path.", action="store", default='ping.log')
args = parser.parse_args()

epoch = datetime.datetime(1970, 1, 1)

file1 = open(args.path, 'r')
Lines = file1.readlines()

tfmt = "%Y-%m-%dT%H:%M:%SZ"

def handle_app_start(parts):
    zone = parts[8].replace("(", "").replace(")", "")
    address = parts[7]
    if "True" in parts[-1]:
        value = 1
    else:
        value = -1
    return zone, address, value

def handle_typical_logline(parts):
    zone = parts[3].replace("(", "").replace(")", "")
    address = parts[2]
    if "Dis" not in parts[-1]:
        value = 1
    else:
        value = -1
    return zone, address, value

def convert_to_ts(date_string):
    dt = datetime.datetime.strptime(date_string, tfmt)
    v = (dt - epoch).total_seconds()
    return int(v)

count = 0
out = {
    "internet": {
        "1.1.1.1": {
            "ts": [], 
            "x": [],
            "y": [],
            "connected": 0,
            "disconnected": 0
            },
        "4.2.2.1": {
            "ts": [], 
            "x": [],
            "y": [],
            "connected": 0,
            "disconnected": 0
            },
        "8.8.8.8": {
            "ts": [], 
            "x": [],
            "y": [],
            "connected": 0,
            "disconnected": 0
            }
    },
    "local":{
        "127.0.0.1": {
            "ts": [], 
            "x": [],
            "y": [],
            "connected": 0,
            "disconnected": 0
            },
        "192.168.1.1": {
            "ts": [], 
            "x": [],
            "y": [],
            "connected": 0,
            "disconnected": 0
            },
    }
}

for line in Lines:
    parts = line.split(" ")
    date_string = f"{parts[0]}T{parts[1].split(',')[0]}Z"
    if "Application" in parts[2]:
        zone, address, value = handle_app_start(parts)
    else:
        zone, address, value = handle_typical_logline(parts)
    out[zone][address]["x"].append(convert_to_ts(date_string))
    out[zone][address]["y"].append(value)
    out[zone][address]["ts"].append({"x": convert_to_ts(date_string), "y": value})
    if value == 1:
        out[zone][address]["connected"] += 1
    else:
        out[zone][address]["disconnected"] += 1
    count += 1

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=4)
