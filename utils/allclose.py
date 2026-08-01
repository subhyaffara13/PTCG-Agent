
def allclose(a: ArrayLike, b: ArrayLike, rtol=1e-05, atol=1e-08, equal_nan=False):
    dtype = _dtypes_impl.result_type_impl(a, b)
    a = _util.cast_if_needed(a, dtype)
    b = _util.cast_if_needed(b, dtype)
    return torch.allclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan)


def allclose(
    a: TensorLikeType,
    b: TensorLikeType,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    equal_nan: bool = False,
) -> bool:
    """
    Reference implementation of torch.allclose
    """
    _check_close_args(name="torch.allclose", a=a, b=b, rtol=rtol, atol=atol)

    return bool(
        torch.all(torch.isclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan)).item()
    )


def allclose(types, args, kwargs, process_group):
    return binary_cmp(torch.allclose, types, args, kwargs, process_group)


def allclose(A, B, rtol=1e-05, atol=1e-08):
    if len(A) != len(B):
        return False

    for x, y in zip(A, B):
        if abs(x-y) > atol + rtol * max(abs(x), abs(y)):
            return False
    return True


def allclose(a, b, masked_equal=True, rtol=1e-5, atol=1e-8):
    """
    Returns True if two arrays are element-wise equal within a tolerance.

    This function is equivalent to `allclose` except that masked values
    are treated as equal (default) or unequal, depending on the `masked_equal`
    argument.

    Parameters
    ----------
    a, b : array_like
        Input arrays to compare.
    masked_equal : bool, optional
        Whether masked values in `a` and `b` are considered equal (True) or not
        (False). They are considered equal by default.
    rtol : float, optional
        Relative tolerance. The relative difference is equal to ``rtol * b``.
        Default is 1e-5.
    atol : float, optional
        Absolute tolerance. The absolute difference is equal to `atol`.
        Default is 1e-8.

    Returns
    -------
    y : bool
        Returns True if the two arrays are equal within the given
        tolerance, False otherwise. If either array contains NaN, then
        False is returned.

    See Also
    --------
    all, any
    numpy.allclose : the non-masked `allclose`.

    Notes
    -----
    If the following equation is element-wise True, then `allclose` returns
    True::

      absolute(`a` - `b`) <= (`atol` + `rtol` * absolute(`b`))

    Return True if all elements of `a` and `b` are equal subject to
    given tolerances.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.ma.array([1e10, 1e-7, 42.0], mask=[0, 0, 1])
    >>> a
    masked_array(data=[10000000000.0, 1e-07, --],
                 mask=[False, False,  True],
           fill_value=1e+20)
    >>> b = np.ma.array([1e10, 1e-8, -42.0], mask=[0, 0, 1])
    >>> np.ma.allclose(a, b)
    False

    >>> a = np.ma.array([1e10, 1e-8, 42.0], mask=[0, 0, 1])
    >>> b = np.ma.array([1.00001e10, 1e-9, -42.0], mask=[0, 0, 1])
    >>> np.ma.allclose(a, b)
    True
    >>> np.ma.allclose(a, b, masked_equal=False)
    False

    Masked values are not compared directly.

    >>> a = np.ma.array([1e10, 1e-8, 42.0], mask=[0, 0, 1])
    >>> b = np.ma.array([1.00001e10, 1e-9, 42.0], mask=[0, 0, 1])
    >>> np.ma.allclose(a, b)
    True
    >>> np.ma.allclose(a, b, masked_equal=False)
    False

    """
    x = masked_array(a, copy=False)
    y = masked_array(b, copy=False)

    # make sure y is an inexact type to avoid abs(MIN_INT); will cause
    # casting of x later.
    # NOTE: We explicitly allow timedelta, which used to work. This could
    #       possibly be deprecated. See also gh-18286.
    #       timedelta works if `atol` is an integer or also a timedelta.
    #       Although, the default tolerances are unlikely to be useful
    if y.dtype.kind != "m":
        dtype = np.result_type(y, 1.)
        if y.dtype != dtype:
            y = masked_array(y, dtype=dtype, copy=False)

    m = mask_or(getmask(x), getmask(y))
    xinf = np.isinf(masked_array(x, copy=False, mask=m)).filled(False)
    # If we have some infs, they should fall at the same place.
    if not np.all(xinf == filled(np.isinf(y), False)):
        return False
    # No infs at all
    if not np.any(xinf):
        d = filled(less_equal(absolute(x - y), atol + rtol * absolute(y)),
                   masked_equal)
        return np.all(d)

    if not np.all(filled(x[xinf] == y[xinf], masked_equal)):
        return False
    x = x[~xinf]
    y = y[~xinf]

    d = filled(less_equal(absolute(x - y), atol + rtol * absolute(y)),
               masked_equal)

    return np.all(d)


def allclose(a, b, rtol=1.e-5, atol=1.e-8, equal_nan=False):
    """
    Returns True if two arrays are element-wise equal within a tolerance.

    The tolerance values are positive, typically very small numbers.  The
    relative difference (`rtol` * abs(`b`)) and the absolute difference
    `atol` are added together to compare against the absolute difference
    between `a` and `b`.

    .. warning:: The default `atol` is not appropriate for comparing numbers
                 with magnitudes much smaller than one (see Notes).

    NaNs are treated as equal if they are in the same place and if
    ``equal_nan=True``.  Infs are treated as equal if they are in the same
    place and of the same sign in both arrays.

    Parameters
    ----------
    a, b : array_like
        Input arrays to compare.
    rtol : array_like
        The relative tolerance parameter (see Notes).
    atol : array_like
        The absolute tolerance parameter (see Notes).
    equal_nan : bool
        Whether to compare NaN's as equal.  If True, NaN's in `a` will be
        considered equal to NaN's in `b` in the output array.

    Returns
    -------
    allclose : bool
        Returns True if the two arrays are equal within the given
        tolerance; False otherwise.

    See Also
    --------
    isclose, all, any, equal

    Notes
    -----
    If the following equation is element-wise True, then allclose returns
    True.::

     absolute(a - b) <= (atol + rtol * absolute(b))

    The above equation is not symmetric in `a` and `b`, so that
    ``allclose(a, b)`` might be different from ``allclose(b, a)`` in
    some rare cases.

    The default value of `atol` is not appropriate when the reference value
    `b` has magnitude smaller than one. For example, it is unlikely that
    ``a = 1e-9`` and ``b = 2e-9`` should be considered "close", yet
    ``allclose(1e-9, 2e-9)`` is ``True`` with default settings. Be sure
    to select `atol` for the use case at hand, especially for defining the
    threshold below which a non-zero value in `a` will be considered "close"
    to a very small or zero value in `b`.

    The comparison of `a` and `b` uses standard broadcasting, which
    means that `a` and `b` need not have the same shape in order for
    ``allclose(a, b)`` to evaluate to True.  The same is true for
    `equal` but not `array_equal`.

    `allclose` is not defined for non-numeric data types.
    `bool` is considered a numeric data-type for this purpose.

    Examples
    --------
    >>> import numpy as np
    >>> np.allclose([1e10,1e-7], [1.00001e10,1e-8])
    False

    >>> np.allclose([1e10,1e-8], [1.00001e10,1e-9])
    True

    >>> np.allclose([1e10,1e-8], [1.0001e10,1e-9])
    False

    >>> np.allclose([1.0, np.nan], [1.0, np.nan])
    False

    >>> np.allclose([1.0, np.nan], [1.0, np.nan], equal_nan=True)
    True


    """
    res = all(isclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan))
    return builtins.bool(res)


def allclose(x, y, rtol=1.0000000000000001e-05, atol=1e-08):
    """Returns True if x and y are sufficiently close, elementwise.

    Parameters
    ----------
    rtol : float
        The relative error tolerance.
    atol : float
        The absolute error tolerance.

    """
    # assume finite weights, see numpy.allclose() for reference
    return all(math.isclose(xi, yi, rel_tol=rtol, abs_tol=atol) for xi, yi in zip(x, y))


def allclose(a: ArrayLike, b: ArrayLike, rtol: ArrayLike = 1e-05,
             atol: ArrayLike = 1e-08, equal_nan: bool = False) -> Array:
  r"""Check if two arrays are element-wise approximately equal within a tolerance.

  JAX implementation of :func:`numpy.allclose`.

  Essentially this function evaluates the following condition:

  .. math::

     |a - b| \le \mathtt{atol} + \mathtt{rtol} * |b|

  ``jnp.inf`` in ``a`` will be considered equal to ``jnp.inf`` in ``b``.

  Args:
    a: first input array to compare.
    b: second input array to compare.
    rtol: relative tolerance used for approximate equality. Default = 1e-05.
    atol: absolute tolerance used for approximate equality. Default = 1e-08.
    equal_nan: Boolean. If ``True``, NaNs in ``a`` will be considered
      equal to NaNs in ``b``. Default is ``False``.

  Returns:
    Boolean scalar array indicating whether the input arrays are element-wise
    approximately equal within the specified tolerances.

  See Also:
    - :func:`jax.numpy.isclose`
    - :func:`jax.numpy.equal`

  Examples:
    >>> jnp.allclose(jnp.array([1e6, 2e6, 3e6]), jnp.array([1e6, 2e6, 3e7]))
    Array(False, dtype=bool)
    >>> jnp.allclose(jnp.array([1e6, 2e6, 3e6]),
    ...              jnp.array([1.00008e6, 2.00008e7, 3.00008e8]), rtol=1e3)
    Array(True, dtype=bool)
    >>> jnp.allclose(jnp.array([1e6, 2e6, 3e6]),
    ...              jnp.array([1.00001e6, 2.00002e6, 3.00009e6]), atol=1e3)
    Array(True, dtype=bool)
    >>> jnp.allclose(jnp.array([jnp.nan, 1, 2]),
    ...              jnp.array([jnp.nan, 1, 2]), equal_nan=True)
    Array(True, dtype=bool)
  """
  util.check_arraylike("allclose", a, b)
  return reductions.all(isclose(a, b, rtol, atol, equal_nan))

