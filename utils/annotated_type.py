
def annotated_type(tp: Any, /) -> Any | None:
    """Return the type of the `Annotated` special form, or `None`."""
    return tp.__origin__ if typing_objects.is_annotated(get_origin(tp)) else None

