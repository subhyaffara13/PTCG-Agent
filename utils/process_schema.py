
def process_schema(schema: Any, data: Any, use_default: bool = True) -> tuple[str | None, Any]:
    error = None
    if use_default is True:
        data = default_schema(schema, deepcopy(data))
    try:
        jsonschema.validate(data, schema)
    except Exception as err:
        error = str(err)
    return error, data

