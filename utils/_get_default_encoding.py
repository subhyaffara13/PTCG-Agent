
def _get_default_encoding() -> Any:
    """
    Lazily load and cache the default OpenAI encoding.

    This avoids importing `litellm.litellm_core_utils.default_encoding` (and thus tiktoken)
    at `litellm` import time. The encoding is cached after the first import.

    This is used internally by utils.py functions that need the encoding but shouldn't
    trigger its import during module load.
    """
    global _default_encoding
    if _default_encoding is None:
        from litellm.litellm_core_utils.default_encoding import encoding

        _default_encoding = encoding
    return _default_encoding

