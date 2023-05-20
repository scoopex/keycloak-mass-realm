#!/usr/bin/env python3

import json
import argparse
import uuid
import os

# Specify the path to your JSON file
file_path = "realm-export.json"
namespace = uuid.NAMESPACE_DNS

def find_ids(data, name):
    if isinstance(data, dict):
        for key in data.keys():
            if key == "id":
                data[key] = str(uuid.uuid5(namespace, data[key] + name))

            if isinstance(data[key], dict) or isinstance(data[key], list):
                data[key] = find_ids(data[key], name)

    elif isinstance(data, list):
        for it in range(0, len(data)):
            if isinstance(data[it], dict) or isinstance(data[it], list):
                data[it] = find_ids(data[it], name)
    return data


def create_realm(num, directory):
    name = f"realm%04i" % num
    with open(file_path, 'r') as file:
        data = json.load(file)
        data = find_ids(data, name)
        data["realm"] = name
        with open(f"{directory}/{name}.json", 'w') as file:
            json.dump(data, file, indent=2)


parser = argparse.ArgumentParser(description='Example script with an integer parameter')
parser.add_argument('-n', '--number', type=int, help='Number of reals', required=True)

args = parser.parse_args()

number = args.number

directory = "generated"
if not os.path.exists(directory):
    os.makedirs(directory)

for i in range(1, args.number + 1):
    create_realm(i, directory)
