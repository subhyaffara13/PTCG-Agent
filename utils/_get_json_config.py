import json

def _get_json_config(config_dict):
    """Parse and returns JSON string from python dictionary."""
    json_config = "{}"
    if config_dict is not None:
        json_config = json.dumps(config_dict, sort_keys=True)
    return json_config

