
def _get_token_counter_new() -> Any:
    """
    Lazily load and cache the token_counter function (aliased as token_counter_new).

    This avoids importing `litellm.litellm_core_utils.token_counter` at `litellm` import time.
    The function is cached after the first import.

    This is used internally by utils.py functions that need the token counter but shouldn't
    trigger its import during module load.
    """
    global _token_counter_new_func
    if _token_counter_new_func is None:
        from litellm.litellm_core_utils.token_counter import (
            token_counter as _token_counter_imported,
        )

        _token_counter_new_func = _token_counter_imported
    return _token_counter_new_func

