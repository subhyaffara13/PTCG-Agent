
def _basic_json_schema_validate(
    obj: Any, schema: Dict[str, Any], max_depth: int = 50
) -> bool:
    """
    Basic JSON schema validation without external library.
    Handles: type, required, properties

    Uses an iterative approach with a stack to avoid recursion limits.
    max_depth limits nesting to prevent infinite loops from circular schemas.
    """
    type_map: Dict[str, Union[Type, Tuple[Type, ...]]] = {
        "object": dict,
        "array": list,
        "string": str,
        "number": (int, float),
        "integer": int,
        "boolean": bool,
        "null": type(None),
    }

    # Stack of (obj, schema, depth) tuples to process
    stack: List[Tuple[Any, Dict[str, Any], int]] = [(obj, schema, 0)]

    while stack:
        current_obj, current_schema, depth = stack.pop()

        # Circuit breaker: stop if we've gone too deep
        if depth > max_depth:
            return False

        # Check type
        schema_type = current_schema.get("type")
        if schema_type:
            expected_type = type_map.get(schema_type)
            if expected_type is not None and not isinstance(current_obj, expected_type):
                return False

        # Check required fields and properties for dicts
        if isinstance(current_obj, dict):
            required = current_schema.get("required", [])
            for field in required:
                if field not in current_obj:
                    return False

            # Queue property validations
            properties = current_schema.get("properties", {})
            for prop_name, prop_schema in properties.items():
                if prop_name in current_obj:
                    stack.append((current_obj[prop_name], prop_schema, depth + 1))

    return True

