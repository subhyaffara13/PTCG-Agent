import json

def read_json_file(file):
    with open(file, "r") as fh:
        return json.load(fh)

