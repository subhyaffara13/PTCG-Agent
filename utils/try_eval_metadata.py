
def try_eval_metadata(metadata, name):
    """Evaluate the metadata to a python object, if possible"""
    value = metadata[name]
    if not isinstance(value, str):
        return
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        metadata[name] = value[1:-1]
        return
    if value.startswith("c(") and value.endswith(")"):
        value = "[" + value[2:-1] + "]"
    elif value.startswith("list(") and value.endswith(")"):
        value = "[" + value[5:-1] + "]"
    try:
        metadata[name] = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        if name != "name":
            metadata[name] = "#R_CODE#" + value
        return

