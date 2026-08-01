
def generalized_normal(
  key: ArrayLike,
  p: float,
  shape: Shape = (),
  dtype: DTypeLikeFloat | None = None,
  *,
  out_sharding: NamedSharding | P | None = None,
) -> Array:
  r"""Sample from the generalized normal distribution.

  The values are returned according to the probability density function:

  .. math::
     f(x;p) \propto e^{-|x|^p}

  on the domain :math:`-\infty < x < \infty`, where :math:`p > 0` is the
  shape parameter.

  Args:
    key: a PRNG key used as the random key.
    p: a float representing the shape parameter.
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
    A random array with the specified shape and dtype.
  """
  shape = core.canonicalize_shape(shape)
  key, _ = _check_prng_key("generalized_normal", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  _check_shape("generalized_normal", shape)
  out_sharding = canonicalize_sharding_for_samplers(
      out_sharding, "generalized_normal", shape)
  return maybe_auto_axes(_generalized_normal, out_sharding, shape=shape, dtype=dtype)(key, p)

