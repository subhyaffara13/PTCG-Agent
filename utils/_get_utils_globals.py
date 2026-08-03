import sys

def _get_utils_globals() -> dict:
    """
    Get the globals dictionary of the utils module.

    This is where we cache imported attributes so we don't import them twice.
    When you do `litellm.utils.some_function`, it gets stored in this dictionary.
    """
    return sys.modules["litellm.utils"].__dict__

