
def _set_always_warn_typed_storage_removal(always_warn):
    global _always_warn_typed_storage_removal
    if not isinstance(always_warn, bool):
        raise AssertionError(
            f"always_warn must be bool, got {type(always_warn).__name__}"
        )
    _always_warn_typed_storage_removal = always_warn

