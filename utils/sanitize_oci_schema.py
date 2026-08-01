
def sanitize_oci_schema(schema: Any) -> Any:
    """Recursively remove OCI-incompatible fields from a JSON schema.

    Strips ``title`` keys, removes ``None``-valued ``default`` entries,
    normalises ``type: [T, "null"]`` list types, and ensures arrays carry an
    ``items`` definition.
    """
    if isinstance(schema, list):
        return [sanitize_oci_schema(item) for item in schema]
    if not isinstance(schema, dict):
        return schema

    sanitized: Dict[str, Any] = {}
    for key, value in schema.items():
        if key == "title":
            continue
        if key == "default" and value is None:
            continue
        if key == "type":
            if value == "any":
                sanitized[key] = "object"
                continue
            if isinstance(value, list):
                non_null = [t for t in value if t != "null"]
                sanitized[key] = non_null[0] if non_null else "string"
                continue
        sanitized[key] = sanitize_oci_schema(value)

    if sanitized.get("type") == "array" and "items" not in sanitized:
        sanitized["items"] = {"type": "object"}

    required = sanitized.get("required")
    properties = sanitized.get("properties")
    if "required" in sanitized:
        if isinstance(required, list) and isinstance(properties, dict):
            sanitized["required"] = [
                f for f in required if isinstance(f, str) and f in properties
            ]
        elif not isinstance(required, list):
            sanitized["required"] = []

    return sanitized

