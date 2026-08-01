
def ball(
  key: ArrayLike,
  d: int,
  p: float = 2,
  shape: Shape = (),
  dtype: DTypeLikeFloat | None = None,
  *,
  out_sharding: NamedSharding | P | None = None,
):
  """Sample uniformly from the unit Lp ball.

  Reference: https://arxiv.org/abs/math/0503650.

  Args:
    key: a PRNG key used as the random key.
    d: a nonnegative int representing the dimensionality of the ball.
    p: a float representing the p parameter of the Lp norm.
    shape: optional, the batch dimensions of the result. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    out_sharding: optional, specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array of shape `(*shape, d)` and specified dtype.
  """
  shape = core.canonicalize_shape(shape)
  key, _ = _check_prng_key("ball", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  _check_shape("ball", shape)
  d = core.concrete_or_error(index, d, "The error occurred in jax.random.ball()")
  out_sharding = canonicalize_sharding(out_sharding, "ball")
  return maybe_auto_axes(_ball, out_sharding, d=d,  shape=shape, dtype=dtype)(key, p)

