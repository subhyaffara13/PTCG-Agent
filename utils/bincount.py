
def bincount(x: ArrayLike, /, weights: ArrayLike | None = None, minlength=0):
    if x.numel() == 0:
        # edge case allowed by numpy
        x = x.new_empty(0, dtype=int)

    int_dtype = _dtypes_impl.default_dtypes().int_dtype
    (x,) = _util.typecast_tensors((x,), int_dtype, casting="safe")

    return torch.bincount(x, weights, minlength)


def bincount(
    fake_mode: FakeTensorMode,
    func: OpOverload,
    inputs: FakeTensor,
    weights: FakeTensor | None = None,
    minlength: IntLikeType = 0,
) -> FakeTensor:
    if (
        fake_mode.shape_env is None
        or not fake_mode.shape_env.allow_dynamic_output_shape_ops
    ):
        # Without symints/symfloats, cannot handle this
        raise DynamicOutputShapeException(func)

    new_size = fake_mode.shape_env.create_unbacked_symint()

    from torch.fx.experimental.symbolic_shapes import _constrain_range_for_size

    _constrain_range_for_size(new_size)
    torch._check(new_size >= minlength)
    return inputs.new_empty(new_size)  # type: ignore[return]


def bincount(x, /, weights=None, minlength=0):
    """
    bincount(x, /, weights=None, minlength=0)

    Count number of occurrences of each value in array of non-negative ints.

    The number of bins (of size 1) is one larger than the largest value in
    `x`. If `minlength` is specified, there will be at least this number
    of bins in the output array (though it will be longer if necessary,
    depending on the contents of `x`).
    Each bin gives the number of occurrences of its index value in `x`.
    If `weights` is specified the input array is weighted by it, i.e. if a
    value ``n`` is found at position ``i``, ``out[n] += weight[i]`` instead
    of ``out[n] += 1``.

    Parameters
    ----------
    x : array_like, 1 dimension, nonnegative ints
        Input array.
    weights : array_like, optional
        Weights, array of the same shape as `x`.
    minlength : int, optional
        A minimum number of bins for the output array.

    Returns
    -------
    out : ndarray of ints
        The result of binning the input array.
        The length of `out` is equal to ``np.amax(x)+1``.

    Raises
    ------
    ValueError
        If the input is not 1-dimensional, or contains elements with negative
        values, or if `minlength` is negative.
    TypeError
        If the type of the input is float or complex.

    See Also
    --------
    histogram, digitize, unique

    Examples
    --------
    >>> import numpy as np
    >>> np.bincount(np.arange(5))
    array([1, 1, 1, 1, 1])
    >>> np.bincount(np.array([0, 1, 1, 3, 2, 1, 7]))
    array([1, 3, 1, 1, 0, 0, 0, 1])

    >>> x = np.array([0, 1, 1, 3, 2, 1, 7, 23])
    >>> np.bincount(x).size == np.amax(x)+1
    True

    The input array needs to be of integer dtype, otherwise a
    TypeError is raised:

    >>> np.bincount(np.arange(5, dtype=np.float64))
    Traceback (most recent call last):
      ...
    TypeError: Cannot cast array data from dtype('float64') to dtype('int64')
    according to the rule 'safe'

    A possible use of ``bincount`` is to perform sums over
    variable-size chunks of an array, using the ``weights`` keyword.

    >>> w = np.array([0.3, 0.5, 0.2, 0.7, 1., -0.6]) # weights
    >>> x = np.array([0, 1, 1, 2, 2, 2])
    >>> np.bincount(x,  weights=w)
    array([ 0.3,  0.7,  1.1])

    """
    return (x, weights)


def bincount(x: ArrayLike, weights: ArrayLike | None = None,
             minlength: int = 0, *, length: int | None = None,
             out_sharding: NamedSharding | P | None = None,
             ) -> Array:
  """Count the number of occurrences of each value in an integer array.

  JAX implementation of :func:`numpy.bincount`.

  For an array of non-negative integers ``x``, this function returns an array ``counts``
  of size ``x.max() + 1``, such that ``counts[i]`` contains the number of occurrences
  of the value ``i`` in ``x``.

  The JAX version has a few differences from the NumPy version:

  - In NumPy, passing an array ``x`` with negative entries will result in an error.
    In JAX, negative values are clipped to zero.
  - JAX adds an optional ``length`` parameter which can be used to statically specify
    the length of the output array so that this function can be used with transformations
    like :func:`jax.jit`. In this case, items larger than `length + 1` will be dropped.

  Args:
    x : 1-dimensional array of non-negative integers
    weights: optional array of weights associated with ``x``. If not specified, the
      weight for each entry will be ``1``.
    minlength: the minimum length of the output counts array.
    length: the length of the output counts array. Must be specified statically for
      ``bincount`` to be used with :func:`jax.jit` and other JAX transformations.
    out_sharding: (optional) :class:`~jax.NamedSharding` or :class:`~jax.P` to
      which the created array will be committed. Use `out_sharding` argument,
      if using explicit sharding (https://docs.jax.dev/en/latest/parallel.html).

  Returns:
    An array of counts or summed weights reflecting the number of occurrences of values
    in ``x``.

  See Also:
    - :func:`jax.numpy.histogram`
    - :func:`jax.numpy.digitize`
    - :func:`jax.numpy.unique_counts`

  Examples:
    Basic bincount:

    >>> x = jnp.array([1, 1, 2, 3, 3, 3])
    >>> jnp.bincount(x)
    Array([0, 2, 1, 3], dtype=int32)

    Weighted bincount:

    >>> weights = jnp.array([1, 2, 3, 4, 5, 6])
    >>> jnp.bincount(x, weights)
    Array([ 0,  3,  3, 15], dtype=int32)

    Specifying a static ``length`` makes this jit-compatible:

    >>> jit_bincount = jax.jit(jnp.bincount, static_argnames=['length'])
    >>> jit_bincount(x, length=5)
    Array([0, 2, 1, 3, 0], dtype=int32)

    Any negative numbers are clipped to the first bin, and numbers beyond the
    specified ``length`` are dropped:

    >>> x = jnp.array([-1, -1, 1, 3, 10])
    >>> jnp.bincount(x, length=5)
    Array([2, 1, 0, 1, 0], dtype=int32)
  """
  x = util.ensure_arraylike("bincount", x)
  if x.dtype == bool:
    x = lax.convert_element_type(x, 'int32')
  if not issubdtype(x.dtype, np.integer):
    raise TypeError(f"x argument to bincount must have an integer type; got {x.dtype}")
  if np.ndim(x) != 1:
    raise ValueError("only 1-dimensional input supported.")
  minlength = core.concrete_or_error(
      operator.index, minlength,
      "The error occurred because of argument 'minlength' of jnp.bincount.")
  if length is None:
    x_arr = core.concrete_or_error(
        asarray, x,
        "The error occurred because of argument 'x' of jnp.bincount. "
        "To avoid this error, pass a static `length` argument.")
    length = max(minlength, x_arr.size and int(max(0, x_arr.max())) + 1)
  else:
    length = core.concrete_dim_or_error(
        length,
        "The error occurred because of argument 'length' of jnp.bincount.")

  if weights is None:
    weights = np.array(1, dtype=dtypes.int_)
  else:
    xts = core.typeof(x).sharding
    wts = core.typeof(weights).sharding
    if (np.shape(x) != np.shape(weights) or
        (not xts.mesh.empty and not wts.mesh.empty and xts != wts)):
      raise ValueError(
          "type of weights must match type of x. Got"
          f" typeof(x)={core.typeof(x).str_short(True, True)} and"
          f" typeof(weights)={core.typeof(weights).str_short(True, True)}")
  out_sharding = canonicalize_sharding(out_sharding, 'jnp.bincount')
  if out_sharding is not None and not is_replicated_or_unreduced(out_sharding):
    raise core.ShardingTypeError(
        "out_sharding passed to `jnp.bincount` can only be fully replicated"
        " or fully unreduced along all mesh axes")
  return array_creation.zeros(length, _dtype(weights)).at[clip(x, 0)].add(
      weights, mode='drop', out_sharding=out_sharding)

