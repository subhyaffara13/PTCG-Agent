
def _block_dispatcher(arrays):
    # Use type(...) is list to match the behavior of np.block(), which special
    # cases list specifically rather than allowing for generic iterables or
    # tuple. Also, we know that list.__array_function__ will never exist.
    if isinstance(arrays, list):
        for subarrays in arrays:
            yield from _block_dispatcher(subarrays)
    else:
        yield arrays

