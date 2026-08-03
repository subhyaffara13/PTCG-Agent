from typing import Any, Dict, List, Union

def normalize_json_schema_types(
    schema: Union[Dict[str, Any], List[Any], Any],
    depth: int = 0,
    max_depth: int = DEFAULT_MAX_RECURSE_DEPTH,
) -> Union[Dict[str, Any], List[Any], Any]:
    """
    Normalize JSON schema types from uppercase to lowercase format.

    Some providers (like certain Google services) use uppercase types like 'BOOLEAN', 'STRING', 'ARRAY', 'OBJECT'
    but standard JSON Schema requires lowercase: 'boolean', 'string', 'array', 'object'

    This function recursively normalizes all type fields in a schema to lowercase.

    Args:
        schema: The schema to normalize (dict, list, or other)
        depth: Current recursion depth
        max_depth: Maximum recursion depth to prevent infinite loops

    Returns:
        The normalized schema with lowercase types
    """
    # Prevent infinite recursion
    if depth >= max_depth:
        return schema

    if not isinstance(schema, (dict, list)):
        return schema

    # Type mapping from uppercase to lowercase
    type_mapping = {
        "BOOLEAN": "boolean",
        "STRING": "string",
        "ARRAY": "array",
        "OBJECT": "object",
        "NUMBER": "number",
        "INTEGER": "integer",
        "NULL": "null",
    }

    if isinstance(schema, list):
        return [
            normalize_json_schema_types(item, depth + 1, max_depth) for item in schema
        ]

    if isinstance(schema, dict):
        normalized_schema: Dict[str, Any] = {}

        for key, value in schema.items():
            if key == "type" and isinstance(value, str) and value in type_mapping:
                normalized_schema[key] = type_mapping[value]
            elif key == "properties" and isinstance(value, dict):
                # Recursively normalize properties
                normalized_schema[key] = {
                    prop_key: normalize_json_schema_types(
                        prop_value, depth + 1, max_depth
                    )
                    for prop_key, prop_value in value.items()
                }
            elif key == "items" and isinstance(value, (dict, list)):
                # Recursively normalize array items
                normalized_schema[key] = normalize_json_schema_types(
                    value, depth + 1, max_depth
                )
            elif isinstance(value, (dict, list)):
                # Recursively normalize any nested dict or list
                normalized_schema[key] = normalize_json_schema_types(
                    value, depth + 1, max_depth
                )
            else:
                normalized_schema[key] = value

        return normalized_schema

    return schema

