
def _get_traceback_str_for_error(error_str: str) -> str:
    """
    function wrapped with lru_cache to limit the number of times `traceback.format_exc()` is called
    """
    return traceback.format_exc()

