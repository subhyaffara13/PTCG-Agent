import os

def _parse_autoheuristic_collect_env():
    collect_env = os.environ.get("TORCHINDUCTOR_AUTOHEURISTIC_COLLECT", "").split(",")
    return collect_env

