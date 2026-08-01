
def sort_complex(a):
    """
    Sort a complex array using the real part first, then the imaginary part.

    Parameters
    ----------
    a : array_like
        Input array

    Returns
    -------
    out : complex ndarray
        Always returns a sorted complex array.

    Examples
    --------
    >>> import numpy as np
    >>> np.sort_complex([5, 3, 6, 2, 1])
    array([1.+0.j, 2.+0.j, 3.+0.j, 5.+0.j, 6.+0.j])

    >>> np.sort_complex([1 + 2j, 2 - 1j, 3 - 2j, 3 - 3j, 3 + 5j])
    array([1.+2.j,  2.-1.j,  3.-3.j,  3.-2.j,  3.+5.j])

    """
    b = array(a, copy=True)
    b.sort()
    if not issubclass(b.dtype.type, _nx.complexfloating):
        if b.dtype.char in 'bhBH':
            return b.astype('F')
        elif b.dtype.char == 'g':
            return b.astype('G')
        else:
            return b.astype('D')
    else:
        return b


def sort_complex(a: ArrayLike) -> Array:
  """Return a sorted copy of complex array.

  JAX implementation of :func:`numpy.sort_complex`.

  Complex numbers are sorted lexicographically, meaning by their real part
  first, and then by their imaginary part if real parts are equal.

  Args:
    a: input array. If dtype is not complex, the array will be upcast to complex.

  Returns:
    A sorted array of the same shape and complex dtype as the input. If ``a``
    is multi-dimensional, it is sorted along the last axis.

  See also:
    - :func:`jax.numpy.sort`: Return a sorted copy of an array.

  Examples:
    >>> a = jnp.array([1+2j, 2+4j, 3-1j, 2+3j])
    >>> jnp.sort_complex(a)
    Array([1.+2.j, 2.+3.j, 2.+4.j, 3.-1.j], dtype=complex64)

    Multi-dimensional arrays are sorted along the last axis:

    >>> a = jnp.array([[5, 3, 4],
    ...                [6, 9, 2]])
    >>> jnp.sort_complex(a)
    Array([[3.+0.j, 4.+0.j, 5.+0.j],
           [2.+0.j, 6.+0.j, 9.+0.j]], dtype=complex64)
  """
  a = util.ensure_arraylike("sort_complex", a)
  a = lax.sort(a)
  return lax.convert_element_type(a, dtypes.to_complex_dtype(a.dtype))

