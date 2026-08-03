import json
import os

def _get_apikey_creds():
    apikey_filename = os.path.expanduser("~/.kaggle/kaggle.json")
    if not os.path.exists(apikey_filename):
        return None

    kaggle_json = None
    with open(apikey_filename) as apikey_file:
        kaggle_json = apikey_file.read()

    if not kaggle_json or not kaggle_json.strip():
        return None

    api_key_data = json.loads(kaggle_json)
    username = api_key_data["username"]
    api_key = api_key_data["key"]
    return username, api_key

