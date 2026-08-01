
def _insert_value(metadata, name, value):
    if value is None:
        return metadata
    metadata[name] = value
    return metadata

