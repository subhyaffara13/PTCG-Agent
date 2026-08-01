
def _register_conversion_cache_cleaner_once():
    atexit.register(_clean_conversion_cache)

