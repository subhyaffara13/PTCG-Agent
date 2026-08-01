
def _fix_enum_empty_strings(schema, depth=0):
    """Fix empty strings in enum values by replacing them with None. Gemini doesn't accept empty strings in enums."""
    if depth > DEFAULT_MAX_RECURSE_DEPTH:
        raise ValueError(
            f"Max depth of {DEFAULT_MAX_RECURSE_DEPTH} exceeded while processing schema."
        )

    if "enum" in schema and isinstance(schema["enum"], list):
        schema["enum"] = [None if value == "" else value for value in schema["enum"]]

    # Reuse existing recursion pattern from convert_anyof_null_to_nullable
    properties = schema.get("properties", None)
    if properties is not None:
        for _, value in properties.items():
            _fix_enum_empty_strings(value, depth=depth + 1)

    items = schema.get("items", None)
    if items is not None:
        _fix_enum_empty_strings(items, depth=depth + 1)

