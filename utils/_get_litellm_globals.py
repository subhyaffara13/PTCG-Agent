import sys

def _get_litellm_globals() -> dict:
    """
    Get the globals dictionary of the litellm module.

    This is where we cache imported attributes so we don't import them twice.
    When you do `litellm.some_function`, it gets stored in this dictionary.
    """
    return sys.modules["litellm"].__dict__

