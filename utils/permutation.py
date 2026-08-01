
def permutation(key: ArrayLike,
                x: int | ArrayLike,
                axis: int = 0,
                independent: bool = False,
                *,
                out_sharding: NamedSharding | P | None = None) -> Array:
  """Returns a randomly permuted array or range.

  Args:
    key: a PRNG key used as the random key.
    x: int or array. If x is an integer, randomly shuffle np.arange(x).
      If x is an array, randomly shuffle its elements.
    axis: int, optional. The axis which x is shuffled along. Default is 0.
    independent: bool, optional. If set to True, each individual vector along
      the given axis is shuffled independently. Default is False.
    out_sharding: Optional. Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A shuffled version of x or array range
  """
  key, _ = _check_prng_key("permutation", key)
  check_arraylike("permutation", x)
  axis = canonicalize_axis(axis, np.ndim(x) or 1)
  out_sharding = canonicalize_sharding(out_sharding, "permutation")
  if not np.ndim(x):
    if not np.issubdtype(lax.dtype(x), np.integer):
      raise TypeError("x must be an integer or at least 1-dimensional")
    r = core.concrete_or_error(int, x, "argument x of jax.random.permutation()")
    return maybe_auto_axes(lambda key: _shuffle(key, jnp.arange(r), axis),
                           out_sharding)(key)
  return maybe_auto_axes(
      _permutation, out_sharding, axis=axis, independent=independent)(key, x)

