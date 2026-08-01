
def _get_cached_slots(obj_type: type) -> tuple[int, int, int, int]:
    """Get all type slots for a type (cached)."""
    return get_type_slots(obj_type)

