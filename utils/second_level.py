
def second_level(keys):
    """Return a dictionary with the nested keys, e.g. returns {'I':['a', 'b']} when keys=['I.a', 'I.b']"""
    sub_keys = {}
    for key in keys:
        if "." in key:
            left, right = key.split(".", 1)
            sub_keys.setdefault(left, []).append(right)

    return sub_keys

