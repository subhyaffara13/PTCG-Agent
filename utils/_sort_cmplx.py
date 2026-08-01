
def _sort_cmplx(arr, xp):
    # xp.sort is undefined for complex dtypes. Here we only need some
    # consistent way to sort a complex array, including equal magnitude elements.
    arr = xp.asarray(arr)
    if xp.isdtype(arr.dtype, 'complex floating'):
        sorter = abs(arr) + xp.real(arr) + xp.imag(arr)**3
    else:
        sorter = arr

    idxs = xp.argsort(sorter)
    return arr[idxs]

