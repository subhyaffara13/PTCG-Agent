
def get_default_val(pat: str):
    key = _get_single_key(pat)
    return _get_registered_option(key).defval

