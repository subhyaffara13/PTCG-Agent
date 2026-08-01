
def extract_by_key(d, keys):
    if isinstance(keys, string_types):
        keys = keys.split()
    result = {}
    for key in keys:
        if key in d:
            result[key] = d[key]
    return result

