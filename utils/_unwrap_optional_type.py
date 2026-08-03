from typing import Any, Union

def _unwrap_optional_type(field_annotation: Any) -> Any:
    """Unwrap Optional types to get the actual type."""
    if (
        hasattr(field_annotation, "__origin__")
        and field_annotation.__origin__ is Union
        and hasattr(field_annotation, "__args__")
    ):
        # For Optional[BaseModel], get the non-None type
        args = field_annotation.__args__
        non_none_args = [arg for arg in args if arg is not type(None)]
        if non_none_args:
            return non_none_args[0]
    return field_annotation

