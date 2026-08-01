
def filter_schema_fields(
    schema_dict: Dict[str, Any], valid_fields: Set[str], processed=None
) -> Dict[str, Any]:
    """
    Recursively filter a schema dictionary to keep only valid fields.
    """
    if processed is None:
        processed = set()

    # Handle circular references
    schema_id = id(schema_dict)
    if schema_id in processed:
        return schema_dict
    processed.add(schema_id)

    if not isinstance(schema_dict, dict):
        return schema_dict

    result = {}
    schema_dict = _filter_anyof_fields(schema_dict)
    for key, value in schema_dict.items():
        if key not in valid_fields:
            continue

        if key == "properties" and isinstance(value, dict):
            result[key] = {
                k: filter_schema_fields(v, valid_fields, processed)
                for k, v in value.items()
            }
        elif key == "format":
            if value in {"enum", "date-time"}:
                result[key] = value
            else:
                continue
        elif key == "items" and isinstance(value, dict):
            result[key] = filter_schema_fields(value, valid_fields, processed)
        elif key == "anyOf" and isinstance(value, list):
            result[key] = [
                filter_schema_fields(item, valid_fields, processed) for item in value  # type: ignore
            ]
        else:
            result[key] = value

    return result

