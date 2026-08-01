
def _has_same_id_matched_objs(frame: DynamoFrameType, cache_entry: Any) -> bool:
    """
    Checks if the ID_MATCH'd objects saved on cache_entry are same as the ones
    in frame.f_locals.
    """
    if not cache_entry:
        return False

    for (
        local_name,
        weakref_from_cache_entry,
    ) in cache_entry.guard_manager.id_matched_objs.items():
        if weakref_from_cache_entry() is not None:
            weakref_from_frame = _get_weakref_from_f_locals(frame, local_name)
            if weakref_from_frame is not weakref_from_cache_entry:
                return False

    # Also covers the case where no ID_MATCH objects are saved in frame.f_locals
    return True

