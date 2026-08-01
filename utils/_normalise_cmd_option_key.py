
def _normalise_cmd_option_key(name: str) -> str:
    return json_compatible_key(name).strip("_=")

