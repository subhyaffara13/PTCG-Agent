
def ndim(a: ArrayLike):
    return a.ndim


def ndim(obj):
    """
    maskedarray version of the numpy function.

    """
    return np.ndim(getdata(obj))


def ndim(a):
    """
    Return the number of dimensions of an array.

    Parameters
    ----------
    a : array_like
        Input array.  If it is not already an ndarray, a conversion is
        attempted.

    Returns
    -------
    number_of_dimensions : int
        The number of dimensions in `a`.  Scalars are zero-dimensional.

    See Also
    --------
    ndarray.ndim : equivalent method
    shape : dimensions of array
    ndarray.shape : dimensions of array

    Examples
    --------
    >>> import numpy as np
    >>> np.ndim([[1,2,3],[4,5,6]])
    2
    >>> np.ndim(np.array([[1,2,3],[4,5,6]]))
    2
    >>> np.ndim(1)
    0

    """
    try:
        return a.ndim
    except AttributeError:
        return asarray(a).ndim


def ndim(a: ArrayLike | SupportsNdim) -> int:
  """Return the number of dimensions of an array.

  JAX implementation of :func:`numpy.ndim`. Unlike ``np.ndim``, this function
  raises a :class:`TypeError` if the input is a collection such as a list or
  tuple.

  Args:
    a: array-like object, or any object with an ``ndim`` attribute.

  Returns:
    An integer specifying the number of dimensions of ``a``.

  Examples:
    Number of dimensions for arrays:

    >>> x = jnp.arange(10)
    >>> jnp.ndim(x)
    1
    >>> y = jnp.ones((2, 3))
    >>> jnp.ndim(y)
    2

    This also works for scalars:

    >>> jnp.ndim(3.14)
    0

    For arrays, this can also be accessed via the :attr:`jax.Array.ndim` property:

    >>> x.ndim
    1
  """
  if hasattr(a, "ndim"):
    return a.ndim
  # Deprecation warning added 2025-2-20.
  check_arraylike("ndim", a, emit_warning=True)
  m = getattr(a, "__jax_array__", None)
  if m is not None:
    a = m()
  # NumPy dispatches to a.ndim if available.
  return np.ndim(a)  # pyrefly: ignore[bad-argument-type]

