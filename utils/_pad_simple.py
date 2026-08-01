
def _pad_simple(array, pad_width, fill_value=None):
    """
    Pad array on all sides with either a single value or undefined values.

    Parameters
    ----------
    array : ndarray
        Array to grow.
    pad_width : sequence of tuple[int, int]
        Pad width on both sides for each dimension in `arr`.
    fill_value : scalar, optional
        If provided the padded area is filled with this value, otherwise
        the pad area left undefined.

    Returns
    -------
    padded : ndarray
        The padded array with the same dtype as`array`. Its order will default
        to C-style if `array` is not F-contiguous.
    original_area_slice : tuple
        A tuple of slices pointing to the area of the original array.
    """
    # Allocate grown array
    new_shape = tuple(
        left + size + right
        for size, (left, right) in zip(array.shape, pad_width)
    )
    order = 'F' if array.flags.fnc else 'C'  # Fortran and not also C-order
    padded = np.empty(new_shape, dtype=array.dtype, order=order)

    if fill_value is not None:
        padded.fill(fill_value)

    # Copy old array into correct space
    original_area_slice = tuple(
        slice(left, left + size)
        for size, (left, right) in zip(array.shape, pad_width)
    )
    padded[original_area_slice] = array

    return padded, original_area_slice

