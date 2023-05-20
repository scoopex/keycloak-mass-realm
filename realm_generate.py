#!/usr/bin/env python3

import json
import argparse
import shutil
import uuid
import os
from typing import Any

namespace = uuid.NAMESPACE_DNS


def find_ids(data: Any, name: str):
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
    else:
        raise RuntimeError("unexpected type {type(data)}")
    return data


def create_realm(num: int, directory: str, template: str):
    name = f"realm%04i" % num
    with open(template, 'r') as file:
        data = json.load(file)
        data = find_ids(data, name)
        data["realm"] = name
        filename = f"{directory}/{name}.json"
        print(f"generating realm {name} to file: {filename}")
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)


rundir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))
file_path = f"{rundir}/realm-export.json"
parser = argparse.ArgumentParser(description='Example script with an integer parameter')
parser.add_argument('-n', '--number', type=int, help='Number of reals', required=True)
parser.add_argument('-t', '--template', type=str, help='The template file', default=file_path)

args = parser.parse_args()

number = args.number

directory = f"{rundir}/generated"
print("recreating directory: " + directory)
if os.path.exists(directory):
    shutil.rmtree(directory)
os.makedirs(directory)

for i in range(1, args.number + 1):
    create_realm(i, directory, args.template)
