
def tensorsolve(a: ArrayLike, b: ArrayLike, axes=None):
    a, b = _atleast_float_2(a, b)
    return torch.linalg.tensorsolve(a, b, dims=axes)


def tensorsolve(a, b, axes=None):
    """
    Solve the tensor equation ``a x = b`` for x.

    It is assumed that all indices of `x` are summed over in the product,
    together with the rightmost indices of `a`, as is done in, for example,
    ``tensordot(a, x, axes=x.ndim)``.

    Parameters
    ----------
    a : array_like
        Coefficient tensor, of shape ``b.shape + Q``. `Q`, a tuple, equals
        the shape of that sub-tensor of `a` consisting of the appropriate
        number of its rightmost indices, and must be such that
        ``prod(Q) == prod(b.shape)`` (in which sense `a` is said to be
        'square').
    b : array_like
        Right-hand tensor, which can be of any shape.
    axes : tuple of ints, optional
        Axes in `a` to reorder to the right, before inversion.
        If None (default), no reordering is done.

    Returns
    -------
    x : ndarray, shape Q

    Raises
    ------
    LinAlgError
        If `a` is singular or not 'square' (in the above sense).

    See Also
    --------
    numpy.tensordot, tensorinv, numpy.einsum

    Examples
    --------
    >>> import numpy as np
    >>> a = np.eye(2*3*4).reshape((2*3, 4, 2, 3, 4))
    >>> rng = np.random.default_rng()
    >>> b = rng.normal(size=(2*3, 4))
    >>> x = np.linalg.tensorsolve(a, b)
    >>> x.shape
    (2, 3, 4)
    >>> np.allclose(np.tensordot(a, x, axes=3), b)
    True

    """
    a, wrap = _makearray(a)
    b = asarray(b)
    an = a.ndim

    if axes is not None:
        allaxes = list(range(an))
        for k in axes:
            allaxes.remove(k)
            allaxes.insert(an, k)
        a = a.transpose(allaxes)

    oldshape = a.shape[-(an - b.ndim):]
    prod = 1
    for k in oldshape:
        prod *= k

    if a.size != prod ** 2:
        raise LinAlgError(
            "Input arrays must satisfy the requirement \
            prod(a.shape[b.ndim:]) == prod(a.shape[:b.ndim])"
        )

    a = a.reshape(prod, prod)
    b = b.ravel()
    res = wrap(solve(a, b))
    return res.reshape(oldshape)


def tensorsolve(a: ArrayLike, b: ArrayLike, axes: tuple[int, ...] | None = None) -> Array:
  """Solve the tensor equation a x = b for x.

  JAX implementation of :func:`numpy.linalg.tensorsolve`.

  Args:
    a: input array. After reordering via ``axes`` (see below), shape must be
      ``(*b.shape, *x.shape)``.
    b: right-hand-side array.
    axes: optional tuple specifying axes of ``a`` that should be moved to the end

  Returns:
    array x such that after reordering of axes of ``a``, ``tensordot(a, x, x.ndim)``
    is equivalent to ``b``.

  See also:
    - :func:`jax.numpy.linalg.tensordot`
    - :func:`jax.numpy.linalg.tensorinv`

  Examples:
    >>> key1, key2 = jax.random.split(jax.random.key(8675309))
    >>> a = jax.random.normal(key1, shape=(2, 2, 4))
    >>> b = jax.random.normal(key2, shape=(2, 2))
    >>> x = jnp.linalg.tensorsolve(a, b)
    >>> x.shape
    (4,)

    Now show that ``x`` can be used to reconstruct ``b`` using
    :func:`~jax.numpy.linalg.tensordot`:

    >>> b_reconstructed = jnp.linalg.tensordot(a, x, axes=x.ndim)
    >>> jnp.allclose(b, b_reconstructed)
    Array(True, dtype=bool)
  """
  a_arr, b_arr = ensure_arraylike("tensorsolve", a, b)
  if axes is not None:
    a_arr = jnp.moveaxis(a_arr, axes, len(axes) * (a_arr.ndim - 1,))
  out_shape = a_arr.shape[b_arr.ndim:]
  if a_arr.shape[:b_arr.ndim] != b_arr.shape:
    raise ValueError("After moving axes to end, leading shape of a must match shape of b."
                     f" got a.shape={a_arr.shape}, b.shape={b_arr.shape}")
  if b_arr.size != math.prod(out_shape):
    raise ValueError("Input arrays must have prod(a.shape[:b.ndim]) == prod(a.shape[b.ndim:]);"
                     f" got a.shape={a_arr.shape}, b.ndim={b_arr.ndim}.")
  a_arr = a_arr.reshape(b_arr.size, math.prod(out_shape))
  return solve(a_arr, b_arr.ravel()).reshape(out_shape)

