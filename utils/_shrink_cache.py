
def _shrink_cache(cache_dict, args_dict, locale_sensitive, max_length, divisor=5):
    """Make room in the given cache.

    Args:
        cache_dict: The cache dictionary to modify.
        args_dict: The dictionary of named list args used by patterns.
        max_length: Maximum # of entries in cache_dict before it is shrunk.
        divisor: Cache will shrink to max_length - 1/divisor*max_length items.
    """
    # Toss out a fraction of the entries at random to make room for new ones.
    # A random algorithm was chosen as opposed to simply cache_dict.popitem()
    # as popitem could penalize the same regular expression repeatedly based
    # on its internal hash value.  Being random should spread the cache miss
    # love around.
    cache_keys = tuple(cache_dict.keys())
    overage = len(cache_keys) - max_length
    if overage < 0:
        # Cache is already within limits.  Normally this should not happen
        # but it could due to multithreading.
        return

    number_to_toss = max_length // divisor + overage

    # The import is done here to avoid a circular dependency.
    import random
    if not hasattr(random, 'sample'):
        # Do nothing while resolving the circular dependency:
        #  re->random->warnings->tokenize->string->re
        return

    for doomed_key in random.sample(cache_keys, number_to_toss):
        try:
            del cache_dict[doomed_key]
        except KeyError:
            # Ignore problems if the cache changed from another thread.
            pass

    # Rebuild the arguments and locale-sensitivity dictionaries.
    args_dict.clear()
    sensitivity_dict = {}
    for pattern, pattern_type, flags, args, default_version, locale in tuple(cache_dict):
        args_dict[pattern, pattern_type, flags, default_version, locale] = args
        try:
            sensitivity_dict[pattern_type, pattern] = locale_sensitive[pattern_type, pattern]
        except KeyError:
            pass

    locale_sensitive.clear()
    locale_sensitive.update(sensitivity_dict)

