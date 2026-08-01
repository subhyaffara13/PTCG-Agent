
def unique_values(x: Array, /, xp: Namespace) -> Array:
    kwargs = _unique_kwargs(xp)
    return xp.unique(
        x,
        return_counts=False,
        return_index=False,
        return_inverse=False,
        **kwargs,
    )


def unique_values(x: Array) -> Array:
    return torch.unique(x)


def unique_values(x):
    """
    Returns the unique elements of an input array `x`.

    This function is an Array API compatible alternative to::

        np.unique(x, equal_nan=False, sorted=False)

    .. versionchanged:: 2.3
       The algorithm was changed to a faster one that does not rely on
       sorting, and hence the results are no longer implicitly sorted.

    Parameters
    ----------
    x : array_like
        Input array. It will be flattened if it is not already 1-D.

    Returns
    -------
    out : ndarray
        The unique elements of an input array.

    See Also
    --------
    unique : Find the unique elements of an array.

    Examples
    --------
    >>> import numpy as np
    >>> np.unique_values([1, 1, 2])
    array([1, 2])  # may vary

    """
    return unique(
        x,
        return_index=False,
        return_inverse=False,
        return_counts=False,
        equal_nan=False,
        sorted=False,
    )


def unique_values(x: ArrayLike, /, *, size: int | None = None,
                  fill_value: ArrayLike | None = None) -> Array:
  """Return unique values from x, along with indices, inverse indices, and counts.

  JAX implementation of :func:`numpy.unique_values`; this is equivalent to calling
  :func:`jax.numpy.unique` with `equal_nan` set to True.

  Because the size of the output of ``unique_values`` is data-dependent, the function
  is not typically compatible with :func:`~jax.jit` and other JAX transformations.
  The JAX version adds the optional ``size`` argument which must be specified statically
  for ``jnp.unique`` to be used in such contexts.

  Args:
    x: N-dimensional array from which unique values will be extracted.
    size: if specified, return only the first ``size`` sorted unique elements. If there are fewer
      unique elements than ``size`` indicates, the return value will be padded with ``fill_value``.
    fill_value: when ``size`` is specified and there are fewer than the indicated number of
      elements, fill the remaining entries ``fill_value``. Defaults to the minimum unique value.

  Returns:
    An array ``values`` of shape ``(n_unique,)`` containing the unique values from ``x``.

  See also:
    - :func:`jax.numpy.unique`: general function for computing unique values.
    - :func:`jax.numpy.unique_values`: compute only ``values``.
    - :func:`jax.numpy.unique_counts`: compute only ``values`` and ``counts``.
    - :func:`jax.numpy.unique_inverse`: compute only ``values`` and ``inverse``.

  Examples:
    Here we compute the unique values in a 1D array:

    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> jnp.unique_values(x)
    Array([1, 3, 4], dtype=int32)

    For examples of the ``size`` and ``fill_value`` arguments, see :func:`jax.numpy.unique`.
  """
  x = ensure_arraylike("unique_values", x)
  return cast(Array, unique(x, equal_nan=False, size=size, fill_value=fill_value))

