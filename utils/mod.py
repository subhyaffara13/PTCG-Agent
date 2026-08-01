
def mod(a, values):
    """
    Return (a % i), that is pre-Python 2.6 string formatting
    (interpolation), element-wise for a pair of array_likes of str
    or unicode.

    Parameters
    ----------
    a : array_like, with ``bytes_`` or ``str_`` dtype

    values : array_like of values
       These values will be element-wise interpolated into the string.

    Returns
    -------
    out : ndarray
        Output array of ``StringDType``, ``bytes_`` or ``str_`` dtype,
        depending on input types

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(["NumPy is a %s library"])
    >>> np.strings.mod(a, values=["Python"])
    array(['NumPy is a Python library'], dtype='<U25')

    >>> a = np.array([b'%d bytes', b'%d bits'])
    >>> values = np.array([8, 64])
    >>> np.strings.mod(a, values)
    array([b'8 bytes', b'64 bits'], dtype='|S7')

    """
    return _to_bytes_or_str_array(
        _vec_string(a, np.object_, '__mod__', (values,)), a)


def mod(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.remainder`"""
  return remainder(x1, x2)

