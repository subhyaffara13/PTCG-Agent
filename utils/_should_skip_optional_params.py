
def _should_skip_optional_params(field_name: str, field_annotation: Any) -> bool:
    """Check if optional_params field should be skipped (not meaningfully overridden)."""
    if field_name != "optional_params":
        return False

    if field_annotation is None:
        return True

    # Check if the annotation is still a generic TypeVar (not specialized)
    if isinstance(field_annotation, TypeVar) or (
        hasattr(field_annotation, "__origin__")
        and field_annotation.__origin__ is TypeVar
    ):
        return True

    # Also skip if it's a generic type that wasn't specialized
    if hasattr(field_annotation, "__name__") and field_annotation.__name__ in (
        "T",
        "TypeVar",
    ):
        return True

    # Handle Optional[T] where T is still a TypeVar
    if hasattr(field_annotation, "__args__"):
        non_none_args = [
            arg for arg in field_annotation.__args__ if arg is not type(None)
        ]
        if non_none_args and isinstance(non_none_args[0], TypeVar):
            return True

    return False

