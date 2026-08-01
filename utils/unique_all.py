
def unique_all(x: Array, /, xp: Namespace) -> UniqueAllResult:
    kwargs = _unique_kwargs(xp)
    values, indices, inverse_indices, counts = xp.unique(
        x,
        return_counts=True,
        return_index=True,
        return_inverse=True,
        **kwargs,
    )
    # np.unique() flattens inverse indices, but they need to share x's shape
    # See https://github.com/numpy/numpy/issues/20638
    inverse_indices = inverse_indices.reshape(x.shape)
    return UniqueAllResult(
        values,
        indices,
        inverse_indices,
        counts,
    )


def unique_all(x: Array) -> UniqueAllResult:
    # torch.unique doesn't support returning indices.
    # https://github.com/pytorch/pytorch/issues/36748. The workaround
    # suggested in that issue doesn't actually function correctly (it relies
    # on non-deterministic behavior of scatter()).
    raise NotImplementedError("unique_all() not yet implemented for pytorch (see https://github.com/pytorch/pytorch/issues/36748)")


def unique_all(x):
    """
    Find the unique elements of an array, and counts, inverse, and indices.

    This function is an Array API compatible alternative to::

        np.unique(x, return_index=True, return_inverse=True,
                  return_counts=True, equal_nan=False, sorted=False)

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
        * indices - The first occurring indices for each unique element.
        * inverse_indices - The indices from the set of unique elements
          that reconstruct `x`.
        * counts - The corresponding counts for each unique element.

    See Also
    --------
    unique : Find the unique elements of an array.

    Examples
    --------
    >>> import numpy as np
    >>> x = [1, 1, 2]
    >>> uniq = np.unique_all(x)
    >>> uniq.values
    array([1, 2])
    >>> uniq.indices
    array([0, 2])
    >>> uniq.inverse_indices
    array([0, 0, 1])
    >>> uniq.counts
    array([2, 1])
    """
    result = unique(
        x,
        return_index=True,
        return_inverse=True,
        return_counts=True,
        equal_nan=False,
    )
    return UniqueAllResult(*result)


def unique_all(x: ArrayLike, /, *, size: int | None = None,
               fill_value: ArrayLike | None = None) -> _UniqueAllResult:
  """Return unique values from x, along with indices, inverse indices, and counts.

  JAX implementation of :func:`numpy.unique_all`; this is equivalent to calling
  :func:`jax.numpy.unique` with `return_index`, `return_inverse`, `return_counts`,
  and `equal_nan` set to True.

  Because the size of the output of ``unique_all`` is data-dependent, the function
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
    - ``indices``:
        An array of shape ``(n_unique,)``. Contains the indices of the first occurrence of
        each unique value in ``x``. For 1D inputs, ``x[indices]`` is equivalent to ``values``.
    - ``inverse_indices``:
        An array of shape ``x.shape``. Contains the indices within ``values`` of each value
        in ``x``. For 1D inputs, ``values[inverse_indices]`` is equivalent to ``x``.
    - ``counts``:
        An array of shape ``(n_unique,)``. Contains the number of occurrences of each unique
        value in ``x``.

  See also:
    - :func:`jax.numpy.unique`: general function for computing unique values.
    - :func:`jax.numpy.unique_values`: compute only ``values``.
    - :func:`jax.numpy.unique_counts`: compute only ``values`` and ``counts``.
    - :func:`jax.numpy.unique_inverse`: compute only ``values`` and ``inverse``.

  Examples:
    Here we compute the unique values in a 1D array:

    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> result = jnp.unique_all(x)

    The result is a :class:`~typing.NamedTuple` with four named attributes.
    The ``values`` attribute contains the unique values from the array:

    >>> result.values
    Array([1, 3, 4], dtype=int32)

    The ``indices`` attribute contains the indices of the unique ``values`` within
    the input array:

    >>> result.indices
    Array([2, 0, 1], dtype=int32)
    >>> jnp.all(result.values == x[result.indices])
    Array(True, dtype=bool)

    The ``inverse_indices`` attribute contains the indices of the input within ``values``:

    >>> result.inverse_indices
    Array([1, 2, 0, 1, 0], dtype=int32)
    >>> jnp.all(x == result.values[result.inverse_indices])
    Array(True, dtype=bool)

    The ``counts`` attribute contains the counts of each unique value in the input:

    >>> result.counts
    Array([2, 2, 1], dtype=int32)

    For examples of the ``size`` and ``fill_value`` arguments, see :func:`jax.numpy.unique`.
  """
  x = ensure_arraylike("unique_all", x)
  values, indices, inverse_indices, counts = unique(
    x, return_index=True, return_inverse=True, return_counts=True, equal_nan=False,
    size=size, fill_value=fill_value)
  return _UniqueAllResult(values=values, indices=indices, inverse_indices=inverse_indices, counts=counts)

