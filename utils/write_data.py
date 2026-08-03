import json

def write_data():
    """Writes the current res_dict to the target JSON file"""
    with open(results_filepath, mode="w") as f:
        json.dump(res_dict, f, indent=2)

