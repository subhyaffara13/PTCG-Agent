
def isposinf(x: ArrayLike, out: OutArray | None = None):
    return torch.isposinf(x)


def isposinf(a: TensorLikeType) -> TensorLikeType:
    torch._check(
        not utils.is_complex_dtype(a.dtype),
        lambda: f"Complex dtype is not supported for isposinf, got dtype {a.dtype}",
    )
    if utils.is_float_dtype(a.dtype):
        return a == float("inf")
    return torch.zeros_like(a, dtype=torch.bool)


def isposinf(x, out=None):
    """
    Test element-wise for positive infinity, return result as bool array.

    Parameters
    ----------
    x : array_like
        The input array.
    out : array_like, optional
        A location into which the result is stored. If provided, it must have a
        shape that the input broadcasts to. If not provided or None, a
        freshly-allocated boolean array is returned.

    Returns
    -------
    out : ndarray
        A boolean array with the same dimensions as the input.
        If second argument is not supplied then a boolean array is returned
        with values True where the corresponding element of the input is
        positive infinity and values False where the element of the input is
        not positive infinity.

        If a second argument is supplied the result is stored there. If the
        type of that array is a numeric type the result is represented as zeros
        and ones, if the type is boolean then as False and True.
        The return value `out` is then a reference to that array.

    See Also
    --------
    isinf, isneginf, isfinite, isnan

    Notes
    -----
    NumPy uses the IEEE Standard for Binary Floating-Point for Arithmetic
    (IEEE 754).

    Errors result if the second argument is also supplied when x is a scalar
    input, if first and second arguments have different shapes, or if the
    first argument has complex values

    Examples
    --------
    >>> import numpy as np
    >>> np.isposinf(np.inf)
    True
    >>> np.isposinf(-np.inf)
    False
    >>> np.isposinf([-np.inf, 0., np.inf])
    array([False, False,  True])

    >>> x = np.array([-np.inf, 0., np.inf])
    >>> y = np.array([2, 2, 2])
    >>> np.isposinf(x, y)
    array([0, 0, 1])
    >>> y
    array([0, 0, 1])

    """
    is_inf = nx.isinf(x)
    try:
        signbit = ~nx.signbit(x)
    except TypeError as e:
        dtype = nx.asanyarray(x).dtype
        raise TypeError(f'This operation is not supported for {dtype} values '
                        'because it would be ambiguous.') from e
    else:
        return nx.logical_and(is_inf, signbit, out)


def isposinf(x, /, out=None):
  """
  Return boolean array indicating whether each element of input is positive infinite.

  JAX implementation of :obj:`numpy.isposinf`.

  Args:
    x: input array or scalar. ``complex`` dtype are not supported.

  Returns:
    A boolean array of same shape as ``x`` containing ``True`` where ``x`` is
    ``inf``, and ``False`` otherwise.

  See also:
    - :func:`jax.numpy.isinf`: Returns a boolean array indicating whether each
      element of input is either positive or negative infinity.
    - :func:`jax.numpy.isneginf`: Returns a boolean array indicating whether each
      element of input is negative infinity.
    - :func:`jax.numpy.isfinite`: Returns a boolean array indicating whether each
      element of input is finite.
    - :func:`jax.numpy.isnan`: Returns a boolean array indicating whether each
      element of input is not a number (``NaN``).

  Examples:
    >>> jnp.isposinf(5)
    Array(False, dtype=bool)
    >>> x = jnp.array([-jnp.inf, 5, jnp.inf, jnp.nan, 1])
    >>> jnp.isposinf(x)
    Array([False, False,  True, False, False], dtype=bool)
  """
  x = ensure_arraylike("isposinf", x)
  return _isposneginf(np.inf, x, out)

