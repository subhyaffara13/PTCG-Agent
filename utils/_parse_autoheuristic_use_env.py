
def _parse_autoheuristic_use_env():
    use_env = os.environ.get("TORCHINDUCTOR_AUTOHEURISTIC_USE", "mixed_mm").split(",")
    return use_env

