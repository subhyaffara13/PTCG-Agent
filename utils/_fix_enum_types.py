
def _fix_enum_types(schema, depth=0):
    """Remove `enum` fields when the schema type is not string.

    Gemini / Vertex APIs only allow enums for string-typed fields. When an enum
    is present on a non-string typed property (or when `anyOf` types do not
    include a string type), remove the enum to avoid provider validation errors.
    """
    if depth > DEFAULT_MAX_RECURSE_DEPTH:
        raise ValueError(
            f"Max depth of {DEFAULT_MAX_RECURSE_DEPTH} exceeded while processing schema."
        )

    if not isinstance(schema, dict):
        return

    # If enum exists but type is not string (and anyOf doesn't include string), drop enum
    if "enum" in schema and isinstance(schema["enum"], list):
        schema_type = schema.get("type")
        keep_enum = False
        if isinstance(schema_type, str) and schema_type.lower() == "string":
            keep_enum = True
        else:
            anyof = schema.get("anyOf")
            if isinstance(anyof, list):
                for item in anyof:
                    if isinstance(item, dict):
                        item_type = item.get("type")
                        if isinstance(item_type, str) and item_type.lower() == "string":
                            keep_enum = True
                            break

        if not keep_enum:
            schema.pop("enum", None)

    # Recurse into nested structures
    properties = schema.get("properties", None)
    if properties is not None:
        for _, value in properties.items():
            _fix_enum_types(value, depth=depth + 1)

    items = schema.get("items", None)
    if items is not None:
        _fix_enum_types(items, depth=depth + 1)

    anyof = schema.get("anyOf", None)
    if anyof is not None and isinstance(anyof, list):
        for item in anyof:
            if isinstance(item, dict):
                _fix_enum_types(item, depth=depth + 1)

