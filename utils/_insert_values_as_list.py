
def _insert_values_as_list(metadata, name, values):
    if values is None:
        return metadata
    if isinstance(values, str):
        values = [values]
    values = [v for v in values if v is not None]
    if len(values) == 0:
        return metadata
    metadata[name] = values
    return metadata

