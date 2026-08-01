
def process_items(schema, depth=0):
    if depth > DEFAULT_MAX_RECURSE_DEPTH:
        raise ValueError(
            f"Max depth of {DEFAULT_MAX_RECURSE_DEPTH} exceeded while processing schema. Please check the schema for excessive nesting."
        )
    if isinstance(schema, dict):
        # Vertex requires `items` whenever `type == "array"` (even inside anyOf).
        # Normalize: empty `items: {}` and missing-items both become {"type": "object"}.
        type_val = schema.get("type")
        if (
            isinstance(type_val, str)
            and type_val.lower() == "array"
            and ("items" not in schema or schema.get("items") == {})
        ):
            schema["items"] = {"type": "object"}
        elif schema.get("type") == "array" and "items" not in schema:
            schema["items"] = {"type": "object"}
        for key, value in schema.items():
            if isinstance(value, dict):
                process_items(value, depth + 1)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        process_items(item, depth + 1)

