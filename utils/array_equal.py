
def array_equal(a1: ArrayLike, a2: ArrayLike, equal_nan=False):
    return _tensor_equal(a1, a2, equal_nan=equal_nan)


def array_equal(a1, a2, equal_nan=False):
    """
    True if two arrays have the same shape and elements, False otherwise.

    Parameters
    ----------
    a1, a2 : array_like
        Input arrays.
    equal_nan : bool
        Whether to compare NaN's as equal. If the dtype of a1 and a2 is
        complex, values will be considered equal if either the real or the
        imaginary component of a given value is ``nan``.

    Returns
    -------
    b : bool
        Returns True if the arrays are equal.

    See Also
    --------
    allclose: Returns True if two arrays are element-wise equal within a
              tolerance.
    array_equiv: Returns True if input arrays are shape consistent and all
                 elements equal.

    Examples
    --------
    >>> import numpy as np

    >>> np.array_equal([1, 2], [1, 2])
    True

    >>> np.array_equal(np.array([1, 2]), np.array([1, 2]))
    True

    >>> np.array_equal([1, 2], [1, 2, 3])
    False

    >>> np.array_equal([1, 2], [1, 4])
    False

    >>> a = np.array([1, np.nan])
    >>> np.array_equal(a, a)
    False

    >>> np.array_equal(a, a, equal_nan=True)
    True

    When ``equal_nan`` is True, complex values with nan components are
    considered equal if either the real *or* the imaginary components are nan.

    >>> a = np.array([1 + 1j])
    >>> b = a.copy()
    >>> a.real = np.nan
    >>> b.imag = np.nan
    >>> np.array_equal(a, b, equal_nan=True)
    True
    """
    try:
        a1, a2 = asarray(a1), asarray(a2)
    except Exception:
        return False
    if a1.shape != a2.shape:
        return False
    if not equal_nan:
        return builtins.bool((asanyarray(a1 == a2)).all())

    if a1 is a2:
        # nan will compare equal so an array will compare equal to itself.
        return True

    cannot_have_nan = (_dtype_cannot_hold_nan(a1.dtype)
                       and _dtype_cannot_hold_nan(a2.dtype))
    if cannot_have_nan:
        return builtins.bool(asarray(a1 == a2).all())

    # Fast path for a1 and a2 being all NaN arrays
    a1nan = isnan(a1)
    if a1nan.all():
        return builtins.bool(isnan(a2).all())

    equal_or_both_nan = (a1 == a2) | (a1nan & isnan(a2))
    return builtins.bool(equal_or_both_nan.all())


def array_equal(a1: ArrayLike, a2: ArrayLike, equal_nan: bool = False) -> Array:
  """Check if two arrays are element-wise equal.

  JAX implementation of :func:`numpy.array_equal`.

  Args:
    a1: first input array to compare.
    a2: second input array to compare.
    equal_nan: Boolean. If ``True``, NaNs in ``a1`` will be considered
      equal to NaNs in ``a2``. Default is ``False``.

  Returns:
    Boolean scalar array indicating whether the input arrays are element-wise equal.

  See Also:
    - :func:`jax.numpy.allclose`
    - :func:`jax.numpy.array_equiv`

  Examples:
    >>> jnp.array_equal(jnp.array([1, 2, 3]), jnp.array([1, 2, 3]))
    Array(True, dtype=bool)
    >>> jnp.array_equal(jnp.array([1, 2, 3]), jnp.array([1, 2]))
    Array(False, dtype=bool)
    >>> jnp.array_equal(jnp.array([1, 2, 3]), jnp.array([1, 2, 4]))
    Array(False, dtype=bool)
    >>> jnp.array_equal(jnp.array([1, 2, float('nan')]),
    ...                 jnp.array([1, 2, float('nan')]))
    Array(False, dtype=bool)
    >>> jnp.array_equal(jnp.array([1, 2, float('nan')]),
    ...                 jnp.array([1, 2, float('nan')]), equal_nan=True)
    Array(True, dtype=bool)
  """
  a1, a2 = asarray(a1), asarray(a2)
  if np.shape(a1) != np.shape(a2):
    return array(False, dtype=bool)
  eq = asarray(a1 == a2)
  if equal_nan:
    eq = ufuncs.logical_or(eq, ufuncs.logical_and(ufuncs.isnan(a1), ufuncs.isnan(a2)))
  return reductions.all(eq)

