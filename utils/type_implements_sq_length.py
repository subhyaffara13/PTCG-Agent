
def type_implements_sq_length(obj_type: type) -> bool:
    """Check whether obj_type implements __len__ as sequence protocol"""
    seq_slots, _, _, _ = _get_cached_slots(obj_type)
    return has_slot(seq_slots, PySequenceSlots.SQ_LENGTH)

