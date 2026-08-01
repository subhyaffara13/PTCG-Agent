
def _get_dict_value_type(field_annotation: Any) -> str:
    """
    Get the value type from Dict[K, V] types
    """
    if (
        hasattr(field_annotation, "__origin__")
        and field_annotation.__origin__ is dict
        and hasattr(field_annotation, "__args__")
    ):
        args = field_annotation.__args__
        if len(args) >= 2:
            value_type = args[1]
            return _get_field_type_from_annotation(value_type)
    return "string"

