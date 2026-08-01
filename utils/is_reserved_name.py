
def is_reserved_name(name):
    return name.startswith(_reserved_prefix) or name in _reserved_names

