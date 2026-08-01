
def _build_field_dict(
    field: Any,
    field_annotation: Any,
    description: str,
    required: bool,
) -> Dict[str, Any]:
    """Build field dictionary for non-nested fields."""
    # Determine the field type from annotation
    field_type = _get_field_type_from_annotation(field_annotation)

    # Check for custom UI type override
    field_json_schema_extra = getattr(field, "json_schema_extra", {})
    if field_json_schema_extra and "ui_type" in field_json_schema_extra:
        ui_type = field_json_schema_extra["ui_type"]
        field_type = ui_type.value if hasattr(ui_type, "value") else ui_type
    elif field_json_schema_extra and "type" in field_json_schema_extra:
        field_type = field_json_schema_extra["type"]

    # Add the field to the dictionary
    field_dict = {
        "description": description,
        "required": required,
        "type": field_type,
    }

    # Extract options from type annotations
    if field_type == "dict":
        # For Dict[Literal[...], T] types, extract key options
        dict_key_options = _get_dict_key_options(field_annotation)
        if dict_key_options:
            field_dict["dict_key_options"] = dict_key_options

        # Extract value type for the dict values
        dict_value_type = _get_dict_value_type(field_annotation)
        field_dict["dict_value_type"] = dict_value_type

    elif field_type == "array":
        # For List[Literal[...]] types, extract element options
        list_element_options = _get_list_element_options(field_annotation)
        if list_element_options:
            field_dict["options"] = list_element_options
            field_dict["type"] = "multiselect"

    # Add options if they exist in json_schema_extra (this takes precedence)
    if field_json_schema_extra and "options" in field_json_schema_extra:
        field_dict["options"] = field_json_schema_extra["options"]
    elif field_type == "select":
        # For Literal types, populate options so the UI can render a dropdown
        literal_options = _extract_literal_values(field_annotation)
        if literal_options:
            field_dict["options"] = literal_options

    # Add default value if it exists
    if field.default is not None and field.default is not ...:
        field_dict["default_value"] = field.default

    # Copy min, max, step from json_schema_extra for number/percentage inputs
    if field_json_schema_extra:
        for key in ("min", "max", "step", "default_value"):
            if key in field_json_schema_extra:
                field_dict[key] = field_json_schema_extra[key]

    return field_dict

