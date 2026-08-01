
def _get_field_type_from_annotation(field_annotation: Any) -> str:
    """
    Convert a Python type annotation to a UI-friendly type string
    """
    # Handle Union types (like Optional[T])
    if (
        hasattr(field_annotation, "__origin__")
        and field_annotation.__origin__ is Union
        and hasattr(field_annotation, "__args__")
    ):
        # For Optional[T], get the non-None type
        args = field_annotation.__args__
        non_none_args = [arg for arg in args if arg is not type(None)]
        if non_none_args:
            field_annotation = non_none_args[0]

    # Handle List types
    if hasattr(field_annotation, "__origin__") and field_annotation.__origin__ is list:
        return "array"

    # Handle Dict types
    if hasattr(field_annotation, "__origin__") and field_annotation.__origin__ is dict:
        return "dict"

    # Handle Literal types
    if hasattr(field_annotation, "__origin__") and hasattr(
        field_annotation, "__args__"
    ):
        # Check for Literal types (Python 3.8+)
        origin = field_annotation.__origin__
        if hasattr(origin, "__name__") and origin.__name__ == "Literal":
            return "select"  # For dropdown/select inputs

    # Handle basic types
    if field_annotation is str:
        return "string"
    elif field_annotation is int:
        return "number"
    elif field_annotation is float:
        return "number"
    elif field_annotation is bool:
        return "boolean"
    elif field_annotation is dict:
        return "object"
    elif field_annotation is list:
        return "array"

    # Default to string for unknown types
    return "string"

