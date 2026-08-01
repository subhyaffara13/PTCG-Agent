
def _is_required_or_notrequired(type_hint: Any) -> bool:
    """Helper to check if a type is Required/NotRequired."""
    return type_hint in (Required, NotRequired) or (get_origin(type_hint) in (Required, NotRequired))

