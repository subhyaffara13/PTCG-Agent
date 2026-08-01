
def unpack_single_str_list(keys):
    # GH 42795
    if isinstance(keys, list) and len(keys) == 1:
        keys = keys[0]
    return keys

