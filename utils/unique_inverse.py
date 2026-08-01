
def unique_inverse(x: Array, /, xp: Namespace) -> UniqueInverseResult:
    kwargs = _unique_kwargs(xp)
    values, inverse_indices = xp.unique(
        x,
        return_counts=False,
        return_index=False,
        return_inverse=True,
        **kwargs,
    )
    # xp.unique() flattens inverse indices, but they need to share x's shape
    # See https://github.com/numpy/numpy/issues/20638
    inverse_indices = inverse_indices.reshape(x.shape)
    return UniqueInverseResult(values, inverse_indices)


def unique_inverse(x: Array) -> UniqueInverseResult:
    values, inverse = torch.unique(x, return_inverse=True)
    return UniqueInverseResult(values, inverse)


def unique_inverse(x):
    """
    Find the unique elements of `x` and indices to reconstruct `x`.

    This function is an Array API compatible alternative to::

        np.unique(x, return_inverse=True, equal_nan=False, sorted=False)

    but returns a namedtuple for easier access to each output.

    .. note::
        This function currently always returns a sorted result, however,
        this could change in any NumPy minor release.

    Parameters
    ----------
    x : array_like
        Input array. It will be flattened if it is not already 1-D.

    Returns
    -------
    out : namedtuple
        The result containing:

        * values - The unique elements of an input array.
        * inverse_indices - The indices from the set of unique elements
          that reconstruct `x`.

    See Also
    --------
    unique : Find the unique elements of an array.

    Examples
    --------
    >>> import numpy as np
    >>> x = [1, 1, 2]
    >>> uniq = np.unique_inverse(x)
    >>> uniq.values
    array([1, 2])
    >>> uniq.inverse_indices
    array([0, 0, 1])
    """
    result = unique(
        x,
        return_index=False,
        return_inverse=True,
        return_counts=False,
        equal_nan=False,
    )
    return UniqueInverseResult(*result)


def unique_inverse(x: ArrayLike, /, *, size: int | None = None,
                   fill_value: ArrayLike | None = None) -> _UniqueInverseResult:
  """Return unique values from x, along with indices, inverse indices, and counts.

  JAX implementation of :func:`numpy.unique_inverse`; this is equivalent to calling
  :func:`jax.numpy.unique` with `return_inverse` and `equal_nan` set to True.

  Because the size of the output of ``unique_inverse`` is data-dependent, the function
  is not typically compatible with :func:`~jax.jit` and other JAX transformations.
  The JAX version adds the optional ``size`` argument which must be specified
  statically for ``jnp.unique`` to be used in such contexts.

  Args:
    x: N-dimensional array from which unique values will be extracted.
    size: if specified, return only the first ``size`` sorted unique elements. If there are fewer
      unique elements than ``size`` indicates, the return value will be padded with ``fill_value``.
    fill_value: when ``size`` is specified and there are fewer than the indicated number of
      elements, fill the remaining entries ``fill_value``. Defaults to the minimum unique value.

  Returns:
    A tuple ``(values, indices, inverse_indices, counts)``, with the following properties:

    - ``values``:
        an array of shape ``(n_unique,)`` containing the unique values from ``x``.
    - ``inverse_indices``:
        An array of shape ``x.shape``. Contains the indices within ``values`` of each value
        in ``x``. For 1D inputs, ``values[inverse_indices]`` is equivalent to ``x``.

  See also:
    - :func:`jax.numpy.unique`: general function for computing unique values.
    - :func:`jax.numpy.unique_values`: compute only ``values``.
    - :func:`jax.numpy.unique_counts`: compute only ``values`` and ``counts``.
    - :func:`jax.numpy.unique_all`: compute ``values``, ``indices``, ``inverse_indices``,
      and ``counts``.

  Examples:
    Here we compute the unique values in a 1D array:

    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> result = jnp.unique_inverse(x)

    The result is a :class:`~typing.NamedTuple` with two named attributes.
    The ``values`` attribute contains the unique values from the array:

    >>> result.values
    Array([1, 3, 4], dtype=int32)

    The ``indices`` attribute contains the indices of the unique ``values`` within
    the input array:

    The ``inverse_indices`` attribute contains the indices of the input within ``values``:

    >>> result.inverse_indices
    Array([1, 2, 0, 1, 0], dtype=int32)
    >>> jnp.all(x == result.values[result.inverse_indices])
    Array(True, dtype=bool)

    For examples of the ``size`` and ``fill_value`` arguments, see :func:`jax.numpy.unique`.
  """
  x = ensure_arraylike("unique_inverse", x)
  values, inverse_indices = unique(x, return_inverse=True, equal_nan=False,
                                   size=size, fill_value=fill_value)
  return _UniqueInverseResult(values=values, inverse_indices=inverse_indices)

