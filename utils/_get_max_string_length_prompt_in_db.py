import os

def _get_max_string_length_prompt_in_db() -> int:
    """
    Resolve prompt truncation threshold at runtime so values loaded later via
    proxy config environment_variables are honored.
    """
    max_length_str = os.getenv("MAX_STRING_LENGTH_PROMPT_IN_DB")
    if max_length_str is None:
        return DEFAULT_MAX_STRING_LENGTH_PROMPT_IN_DB
    try:
        return int(max_length_str)
    except (TypeError, ValueError):
        return DEFAULT_MAX_STRING_LENGTH_PROMPT_IN_DB

