import json

def safe_load_json_file(json_file: str):
    "A helper to load safe config files and raise a proper error message if it wasn't serialized correctly"
    try:
        with open(json_file, encoding="utf-8") as reader:
            text = reader.read()
        config_dict = json.loads(text)
    except json.JSONDecodeError:
        raise OSError(f"It looks like the config file at '{json_file}' is not a valid JSON file.")
    return config_dict

