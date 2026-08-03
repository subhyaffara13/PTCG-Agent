import os

def save_worker_config(**data):
    import json

    os.environ["WORKER_CONFIG"] = json.dumps(data)

