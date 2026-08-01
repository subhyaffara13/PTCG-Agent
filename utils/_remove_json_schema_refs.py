
def _remove_json_schema_refs(schema, max_depth=10):
    """
    Remove JSON schema reference fields like '$id' and '$schema' that can cause issues with some providers.

    These fields are used for schema validation but can cause problems when the schema references
    are not accessible to the provider's validation system.

    Args:
        schema: The schema object to clean (dict, list, or other)
        max_depth: Maximum recursion depth to prevent infinite loops (default: 10)

    Relevant Issues: Mistral API grammar validation fails when schema contains $id and $schema references
    """
    if max_depth <= 0:
        return schema

    if isinstance(schema, dict):
        # Remove JSON schema reference fields
        schema.pop("$id", None)
        schema.pop("$schema", None)

        # Recursively process all dictionary values
        for key, value in schema.items():
            _remove_json_schema_refs(value, max_depth - 1)

    elif isinstance(schema, list):
        # Recursively process all items in the list
        for item in schema:
            _remove_json_schema_refs(item, max_depth - 1)

    return schema

