
def metadata_filter_as_string(metadata_filter):
    """Convert a filter, represented as a dictionary with 'additional' and 'excluded' entries, to a string"""
    if not isinstance(metadata_filter, dict):
        return metadata_filter

    additional = metadata_filter.get("additional", [])
    if additional == "all":
        entries = ["all"]
    else:
        entries = [key for key in additional if key not in _JUPYTEXT_CELL_METADATA]

    excluded = metadata_filter.get("excluded", [])
    if excluded == "all":
        entries.append("-all")
    else:
        entries.extend(["-" + e for e in excluded])

    return ",".join(entries)

