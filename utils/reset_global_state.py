
def reset_global_state() -> None:
    """Reset most existing global state.

    Currently most of it is in this module. Few exceptions are strict optional status
    and functools.lru_cache.
    """
    type_state.reset_all_subtype_caches()
    type_state.reset_protocol_deps()
    TypeVarId.next_raw_id = 1

