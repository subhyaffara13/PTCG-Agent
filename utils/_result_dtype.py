
def _result_dtype(arr):
    # workaround #27953
    # ideally we just pass `dtype=arr.dtype` unconditionally, but this fails
    # when the list of values is empty.
    from pandas.core.arrays.string_ import StringDtype

    if isinstance(arr.dtype, (ArrowDtype, StringDtype)):
        return arr.dtype
    return object

