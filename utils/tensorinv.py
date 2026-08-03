import math


def tensorinv(a: ArrayLike, ind=2):
    a = _atleast_float_1(a)
    return torch.linalg.tensorinv(a, ind=ind)


def tensorinv(a, ind=2):
    """
    Compute the 'inverse' of an N-dimensional array.

    The result is an inverse for `a` relative to the tensordot operation
    ``tensordot(a, b, ind)``, i. e., up to floating-point accuracy,
    ``tensordot(tensorinv(a), a, ind)`` is the "identity" tensor for the
    tensordot operation.

    Parameters
    ----------
    a : array_like
        Tensor to 'invert'. Its shape must be 'square', i. e.,
        ``prod(a.shape[:ind]) == prod(a.shape[ind:])``.
    ind : int, optional
        Number of first indices that are involved in the inverse sum.
        Must be a positive integer, default is 2.

    Returns
    -------
    b : ndarray
        `a`'s tensordot inverse, shape ``a.shape[ind:] + a.shape[:ind]``.

    Raises
    ------
    LinAlgError
        If `a` is singular or not 'square' (in the above sense).

    See Also
    --------
    numpy.tensordot, tensorsolve

    Examples
    --------
    >>> import numpy as np
    >>> a = np.eye(4*6).reshape((4, 6, 8, 3))
    >>> ainv = np.linalg.tensorinv(a, ind=2)
    >>> ainv.shape
    (8, 3, 4, 6)
    >>> rng = np.random.default_rng()
    >>> b = rng.normal(size=(4, 6))
    >>> np.allclose(np.tensordot(ainv, b), np.linalg.tensorsolve(a, b))
    True

    >>> a = np.eye(4*6).reshape((24, 8, 3))
    >>> ainv = np.linalg.tensorinv(a, ind=1)
    >>> ainv.shape
    (8, 3, 24)
    >>> rng = np.random.default_rng()
    >>> b = rng.normal(size=24)
    >>> np.allclose(np.tensordot(ainv, b, 1), np.linalg.tensorsolve(a, b))
    True

    """
    a = asarray(a)
    oldshape = a.shape
    prod = 1
    if ind > 0:
        invshape = oldshape[ind:] + oldshape[:ind]
        for k in oldshape[ind:]:
            prod *= k
    else:
        raise ValueError("Invalid ind argument.")
    a = a.reshape(prod, -1)
    ia = inv(a)
    return ia.reshape(*invshape)


def tensorinv(a: ArrayLike, ind: int = 2) -> Array:
  """Compute the tensor inverse of an array.

  JAX implementation of :func:`numpy.linalg.tensorinv`.

  This computes the inverse of the :func:`~jax.numpy.linalg.tensordot`
  operation with the same ``ind`` value.

  Args:
    a: array to be inverted. Must have ``prod(a.shape[:ind]) == prod(a.shape[ind:])``
    ind: positive integer specifying the number of indices in the tensor product.

  Returns:
    array of shape ``(*a.shape[ind:], *a.shape[:ind])`` containing the
    tensor inverse of ``a``.

  See also:
    - :func:`jax.numpy.linalg.tensordot`
    - :func:`jax.numpy.linalg.tensorsolve`

  Examples:
    >>> key = jax.random.key(1337)
    >>> x = jax.random.normal(key, shape=(2, 2, 4))
    >>> xinv = jnp.linalg.tensorinv(x, 2)
    >>> xinv_x = jnp.linalg.tensordot(xinv, x, axes=2)
    >>> jnp.allclose(xinv_x, jnp.eye(4), atol=1E-4)
    Array(True, dtype=bool)
  """
  arr = ensure_arraylike("tensorinv", a)
  ind = operator.index(ind)
  if ind <= 0:
    raise ValueError(f"ind must be a positive integer; got {ind=}")
  contracting_shape, batch_shape = arr.shape[:ind], arr.shape[ind:]
  flatshape = (math.prod(contracting_shape), math.prod(batch_shape))
  if flatshape[0] != flatshape[1]:
    raise ValueError("tensorinv is only possible when the product of the first"
                     " `ind` dimensions equals that of the remaining dimensions."
                     f" got {arr.shape=} with {ind=}.")
  return inv(arr.reshape(flatshape)).reshape(*batch_shape, *contracting_shape)

