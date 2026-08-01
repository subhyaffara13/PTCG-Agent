
def min_scalar_type(a: ArrayLike, /):
    # https://github.com/numpy/numpy/blob/maintenance/1.24.x/numpy/core/src/multiarray/convert_datatype.c#L1288

    from ._dtypes import DType

    if a.numel() > 1:
        # numpy docs: "For non-scalar array a, returns the vector's dtype unmodified."
        return DType(a.dtype)

    if a.dtype == torch.bool:
        dtype = torch.bool

    elif a.dtype.is_complex:
        fi = torch.finfo(torch.float32)
        fits_in_single = a.dtype == torch.complex64 or (
            fi.min <= a.real <= fi.max and fi.min <= a.imag <= fi.max
        )
        dtype = torch.complex64 if fits_in_single else torch.complex128

    elif a.dtype.is_floating_point:
        for dt in [torch.float16, torch.float32, torch.float64]:
            fi = torch.finfo(dt)
            if fi.min <= a <= fi.max:
                dtype = dt
                break
    else:
        # must be integer
        for dt in [torch.uint8, torch.int8, torch.int16, torch.int32, torch.int64]:
            # Prefer unsigned int where possible, as numpy does.
            ii = torch.iinfo(dt)
            if ii.min <= a <= ii.max:
                dtype = dt
                break

    return DType(dtype)


def min_scalar_type(a, /):
    """
    min_scalar_type(a, /)

    For scalar ``a``, returns the data type with the smallest size
    and smallest scalar kind which can hold its value.  For non-scalar
    array ``a``, returns the vector's dtype unmodified.

    Floating point values are not demoted to integers,
    and complex values are not demoted to floats.

    Parameters
    ----------
    a : scalar or array_like
        The value whose minimal data type is to be found.

    Returns
    -------
    out : dtype
        The minimal data type.

    See Also
    --------
    result_type, promote_types, dtype, can_cast

    Examples
    --------
    >>> import numpy as np
    >>> np.min_scalar_type(10)
    dtype('uint8')

    >>> np.min_scalar_type(-260)
    dtype('int16')

    >>> np.min_scalar_type(3.1)
    dtype('float16')

    >>> np.min_scalar_type(1e50)
    dtype('float64')

    >>> np.min_scalar_type(np.arange(4, dtype=np.float64))
    dtype('float64')

    """
    return (a,)

