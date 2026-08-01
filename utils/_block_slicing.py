
def _block_slicing(arrays, list_ndim, result_ndim):
    shape, slices, arrays = _block_info_recursion(
        arrays, list_ndim, result_ndim)
    dtype = _nx.result_type(*[arr.dtype for arr in arrays])

    # Test preferring F only in the case that all input arrays are F
    F_order = all(arr.flags['F_CONTIGUOUS'] for arr in arrays)
    C_order = all(arr.flags['C_CONTIGUOUS'] for arr in arrays)
    order = 'F' if F_order and not C_order else 'C'
    result = _nx.empty(shape=shape, dtype=dtype, order=order)
    # Note: In a c implementation, the function
    # PyArray_CreateMultiSortedStridePerm could be used for more advanced
    # guessing of the desired order.

    for the_slice, arr in zip(slices, arrays):
        result[(Ellipsis,) + the_slice] = arr
    return result

