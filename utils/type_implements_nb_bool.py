
def type_implements_nb_bool(obj_type: type) -> bool:
    """Check whether obj_type implements the nb_bool slot (i.e. has __bool__ or __len__)."""
    _, _, number_slots, _ = _get_cached_slots(obj_type)
    return has_slot(number_slots, PyNumberSlots.NB_BOOL)

