
def _resolve_name_with_default(name):
    if "." not in name:
        name = "jsonschema." + name
    return resolve_name(name)

