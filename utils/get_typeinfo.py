
def get_typeinfo(name: str, value_name_to_typeinfo: dict) -> fbs.TypeInfo:
    "Lookup a name in a dictionary mapping value name to TypeInfo."
    if name not in value_name_to_typeinfo:
        raise RuntimeError("Missing TypeInfo entry for " + name)

    return value_name_to_typeinfo[name]  # TypeInfo object

