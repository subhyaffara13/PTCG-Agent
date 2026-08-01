
def _new_patcher() -> Iterator[_Patcher]:
    global CURRENT_PATCHER
    prior_patcher = CURRENT_PATCHER
    try:
        CURRENT_PATCHER = _Patcher()
        yield CURRENT_PATCHER
    finally:
        # Clear all the patches made by when using current patcher.
        if CURRENT_PATCHER is None:
            raise AssertionError("CURRENT_PATCHER is None in finally block")
        CURRENT_PATCHER.revert_all_patches()
        CURRENT_PATCHER = prior_patcher

