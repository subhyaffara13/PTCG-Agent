
def double_sided_maxwell(key: ArrayLike,
                         loc: RealArray,
                         scale: RealArray,
                         shape: Shape = (),
                         dtype: DTypeLikeFloat | None = None) -> Array:
  r"""Sample from a double sided Maxwell distribution.

  The values are distributed according to the probability density function:

  .. math::
     f(x;\mu,\sigma) \propto z^2 e^{-z^2 / 2}

  where :math:`z = (x - \mu) / \sigma`, with the center :math:`\mu` specified by
  ``loc`` and the scale :math:`\sigma` specified by ``scale``.

  Args:
    key: a PRNG key.
    loc: The location parameter of the distribution.
    scale: The scale parameter of the distribution.
    shape: The shape added to the parameters loc and scale broadcastable shape.
    dtype: The type used for samples.

  Returns:
    A jnp.array of samples.

  """
  key, _ = _check_prng_key("double_sided_maxwell", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `double_sided_maxwell` must be a float"
                     f" dtype, got {dtype}")
  shape = core.canonicalize_shape(shape)
  return _double_sided_maxwell(key, loc, scale, shape, dtype)

