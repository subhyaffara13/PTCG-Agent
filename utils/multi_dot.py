
def multi_dot(inputs: Sequence[ArrayLike], *, out=None):
    return torch.linalg.multi_dot(inputs)


def multi_dot(arrays, *, out=None):
    """
    Compute the dot product of two or more arrays in a single function call,
    while automatically selecting the fastest evaluation order.

    `multi_dot` chains `numpy.dot` and uses optimal parenthesization
    of the matrices [1]_ [2]_. Depending on the shapes of the matrices,
    this can speed up the multiplication a lot.

    If the first argument is 1-D it is treated as a row vector.
    If the last argument is 1-D it is treated as a column vector.
    The other arguments must be 2-D.

    Think of `multi_dot` as::

        def multi_dot(arrays): return functools.reduce(np.dot, arrays)


    Parameters
    ----------
    arrays : sequence of array_like
        If the first argument is 1-D it is treated as row vector.
        If the last argument is 1-D it is treated as column vector.
        The other arguments must be 2-D.
    out : ndarray, optional
        Output argument. This must have the exact kind that would be returned
        if it was not used. In particular, it must have the right type, must be
        C-contiguous, and its dtype must be the dtype that would be returned
        for `dot(a, b)`. This is a performance feature. Therefore, if these
        conditions are not met, an exception is raised, instead of attempting
        to be flexible.

    Returns
    -------
    output : ndarray
        Returns the dot product of the supplied arrays.

    See Also
    --------
    numpy.dot : dot multiplication with two arguments.

    References
    ----------

    .. [1] Cormen, "Introduction to Algorithms", Chapter 15.2, p. 370-378
    .. [2] https://en.wikipedia.org/wiki/Matrix_chain_multiplication

    Examples
    --------
    `multi_dot` allows you to write::

    >>> import numpy as np
    >>> from numpy.linalg import multi_dot
    >>> # Prepare some data
    >>> A = np.random.random((10000, 100))
    >>> B = np.random.random((100, 1000))
    >>> C = np.random.random((1000, 5))
    >>> D = np.random.random((5, 333))
    >>> # the actual dot multiplication
    >>> _ = multi_dot([A, B, C, D])

    instead of::

    >>> _ = np.dot(np.dot(np.dot(A, B), C), D)
    >>> # or
    >>> _ = A.dot(B).dot(C).dot(D)

    Notes
    -----
    The cost for a matrix multiplication can be calculated with the
    following function::

        def cost(A, B):
            return A.shape[0] * A.shape[1] * B.shape[1]

    Assume we have three matrices
    :math:`A_{10 \\times 100}, B_{100 \\times 5}, C_{5 \\times 50}`.

    The costs for the two different parenthesizations are as follows::

        cost((AB)C) = 10*100*5 + 10*5*50   = 5000 + 2500   = 7500
        cost(A(BC)) = 10*100*50 + 100*5*50 = 50000 + 25000 = 75000

    """
    n = len(arrays)
    # optimization only makes sense for len(arrays) > 2
    if n < 2:
        raise ValueError("Expecting at least two arrays.")
    elif n == 2:
        return dot(arrays[0], arrays[1], out=out)

    arrays = [asanyarray(a) for a in arrays]

    # save original ndim to reshape the result array into the proper form later
    ndim_first, ndim_last = arrays[0].ndim, arrays[-1].ndim
    # Explicitly convert vectors to 2D arrays to keep the logic of the internal
    # _multi_dot_* functions as simple as possible.
    if arrays[0].ndim == 1:
        arrays[0] = atleast_2d(arrays[0])
    if arrays[-1].ndim == 1:
        arrays[-1] = atleast_2d(arrays[-1]).T
    _assert_2d(*arrays)

    # _multi_dot_three is much faster than _multi_dot_matrix_chain_order
    if n == 3:
        result = _multi_dot_three(arrays[0], arrays[1], arrays[2], out=out)
    else:
        order = _multi_dot_matrix_chain_order(arrays)
        result = _multi_dot(arrays, order, 0, n - 1, out=out)

    # return proper shape
    if ndim_first == 1 and ndim_last == 1:
        return result[0, 0]  # scalar
    elif ndim_first == 1 or ndim_last == 1:
        return result.ravel()  # 1-D
    else:
        return result


def multi_dot(arrays: Sequence[ArrayLike], *, precision: lax.PrecisionLike = None) -> Array:
  """Efficiently compute matrix products between a sequence of arrays.

  JAX implementation of :func:`numpy.linalg.multi_dot`.

  JAX internally uses the opt_einsum library to compute the most efficient
  operation order.

  Args:
    arrays: sequence of arrays. All must be two-dimensional, except the first
      and last which may be one-dimensional.
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``).

  Returns:
    an array representing the equivalent of ``reduce(jnp.matmul, arrays)``, but
    evaluated in the optimal order.

  This function exists because the cost of computing sequences of matmul operations
  can differ vastly depending on the order in which the operations are evaluated.
  For a single matmul, the number of floating point operations (flops) required to
  compute a matrix product can be approximated this way:

  >>> def approx_flops(x, y):
  ...   # for 2D x and y, with x.shape[1] == y.shape[0]
  ...   return 2 * x.shape[0] * x.shape[1] * y.shape[1]

  Suppose we have three matrices that we'd like to multiply in sequence:

  >>> key1, key2, key3 = jax.random.split(jax.random.key(0), 3)
  >>> x = jax.random.normal(key1, shape=(200, 5))
  >>> y = jax.random.normal(key2, shape=(5, 100))
  >>> z = jax.random.normal(key3, shape=(100, 10))

  Because of associativity of matrix products, there are two orders in which we might
  evaluate the product ``x @ y @ z``, and both produce equivalent outputs up to floating
  point precision:

  >>> result1 = (x @ y) @ z
  >>> result2 = x @ (y @ z)
  >>> jnp.allclose(result1, result2, atol=1E-4)
  Array(True, dtype=bool)

  But the computational cost of these differ greatly:

  >>> print("(x @ y) @ z flops:", approx_flops(x, y) + approx_flops(x @ y, z))
  (x @ y) @ z flops: 600000
  >>> print("x @ (y @ z) flops:", approx_flops(y, z) + approx_flops(x, y @ z))
  x @ (y @ z) flops: 30000

  The second approach is about 20x more efficient in terms of estimated flops!

  ``multi_dot`` is a function that will automatically choose the fastest
  computational path for such problems:

  >>> result3 = jnp.linalg.multi_dot([x, y, z])
  >>> jnp.allclose(result1, result3, atol=1E-4)
  Array(True, dtype=bool)

  We can use JAX's :ref:`ahead-of-time-lowering` tools to estimate the total flops
  of each approach, and confirm that ``multi_dot`` is choosing the more efficient
  option:

  >>> jax.jit(lambda x, y, z: (x @ y) @ z).lower(x, y, z).cost_analysis()['flops']
  600000.0
  >>> jax.jit(lambda x, y, z: x @ (y @ z)).lower(x, y, z).cost_analysis()['flops']
  30000.0
  >>> jax.jit(jnp.linalg.multi_dot).lower([x, y, z]).cost_analysis()['flops']
  30000.0
  """
  arrs = list(ensure_arraylike('jnp.linalg.multi_dot', *arrays))
  if len(arrs) < 2:
    raise ValueError(f"multi_dot requires at least two arrays; got len(arrays)={len(arrs)}")
  if not (arrs[0].ndim in (1, 2) and arrs[-1].ndim in (1, 2) and
          all(a.ndim == 2 for a in arrs[1:-1])):
    raise ValueError("multi_dot: input arrays must all be two-dimensional, except for"
                     " the first and last array which may be 1 or 2 dimensional."
                     f" Got array shapes {[a.shape for a in arrs]}")
  if any(a.shape[-1] != b.shape[0] for a, b in zip(arrs[:-1], arrs[1:])):
    raise ValueError("multi_dot: last dimension of each array must match first dimension"
                     f" of following array. Got array shapes {[a.shape for a in arrs]}")
  einsum_axes: list[tuple[int, ...]] = [(i, i+1) for i in range(len(arrs))]
  if arrs[0].ndim == 1:
    einsum_axes[0] = einsum_axes[0][1:]
  if arrs[-1].ndim == 1:
    einsum_axes[-1] = einsum_axes[-1][:1]
  return einsum.einsum(*itertools.chain(*zip(arrs, einsum_axes)),  # pyrefly: ignore[no-matching-overload]
                       optimize='auto', precision=precision)

