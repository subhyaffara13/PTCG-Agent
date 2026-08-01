
def _get_schema_json(v, version=None, version_minor=None):
    """
    Gets the json schema from a given imported library and nbformat version.
    """
    if (version, version_minor) in v.nbformat_schema:
        schema_path = str(Path(v.__file__).parent / v.nbformat_schema[(version, version_minor)])
    elif version_minor > v.nbformat_minor:
        # load the latest schema
        schema_path = str(Path(v.__file__).parent / v.nbformat_schema[(None, None)])
    else:
        msg = "Cannot find appropriate nbformat schema file."
        raise AttributeError(msg)
    with Path(schema_path).open(encoding="utf8") as f:
        schema_json = json.load(f)
    return schema_json  # noqa: RET504

