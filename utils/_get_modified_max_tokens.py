from typing import Any

def _get_modified_max_tokens() -> Any:
    """
    Lazily load and cache the get_modified_max_tokens function.

    This avoids importing `litellm.litellm_core_utils.token_counter` at `litellm` import time.
    The function is cached after the first import.

    This is used internally by utils.py functions that need the token counter but shouldn't
    trigger its import during module load.
    """
    global _get_modified_max_tokens_func
    if _get_modified_max_tokens_func is None:
        from litellm.litellm_core_utils.token_counter import (
            get_modified_max_tokens as _get_modified_max_tokens_imported,
        )

        _get_modified_max_tokens_func = _get_modified_max_tokens_imported
    return _get_modified_max_tokens_func

