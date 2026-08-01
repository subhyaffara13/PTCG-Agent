
def _prune_array(array):
    """Return an array equivalent to the input array. If the input
    array is a view of a much larger array, copy its contents to a
    newly allocated array. Otherwise, return the input unchanged.
    """
    if array.base is not None and array.size < array.base.size // 2:
        return array.copy()
    return array

