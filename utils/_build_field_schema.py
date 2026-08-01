
def _build_field_schema(model_class: type) -> Dict[str, Any]:
    """Build field_schema dict from a Pydantic model for UI rendering."""
    schema = TypeAdapter(model_class).json_schema(by_alias=True)
    properties = {}
    for field_name, field_info in schema.get("properties", {}).items():
        properties[field_name] = {
            "description": field_info.get("description", ""),
            "type": _extract_field_type(field_info),
        }
    return {
        "description": schema.get("description", ""),
        "properties": properties,
    }

