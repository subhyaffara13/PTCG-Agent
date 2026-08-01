
def dirichlet(ctx, s, chi=[1], derivative=0):
    s = ctx.convert(s)
    q = len(chi)
    d = int(derivative)
    if d > 2:
        raise NotImplementedError("arbitrary order derivatives")
    prec = ctx.prec
    try:
        ctx.prec += 10
        if s == 1:
            have_pole = True
            for x in chi:
                if x and x != 1:
                    have_pole = False
                    h = +ctx.eps
                    ctx.prec *= 2*(d+1)
                    s += h
            if have_pole:
                return +ctx.inf
        z = ctx.zero
        for p in range(1,q+1):
            if chi[p%q]:
                if d == 1:
                    z += chi[p%q] * (ctx.zeta(s, (p,q), 1) - \
                        ctx.zeta(s, (p,q))*ctx.log(q))
                else:
                    z += chi[p%q] * ctx.zeta(s, (p,q))
        z /= q**s
    finally:
        ctx.prec = prec
    return +z


def dirichlet(key: ArrayLike,
              alpha: RealArray,
              shape: Shape | None = None,
              dtype: DTypeLikeFloat | None = None,
              *,
              out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Dirichlet random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
     f(\{x_i\}; \{\alpha_i\}) \propto \prod_{i=1}^k x_i^{\alpha_i - 1}

  Where :math:`k` is the dimension, and :math:`\{x_i\}` satisfies

  .. math::
     \sum_{i=1}^k x_i = 1

  and :math:`0 \le x_i \le 1` for all :math:`x_i`.

  Args:
    key: a PRNG key used as the random key.
    alpha: an array of shape ``(..., n)`` used as the concentration
      parameter of the random variables.
    shape: optional, a tuple of nonnegative integers specifying the result
      batch shape; that is, the prefix of the result shape excluding the last
      element of value ``n``. Must be broadcast-compatible with
      ``alpha.shape[:-1]``. The default (None) produces a result shape equal to
      ``alpha.shape``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    out_sharding: Optional. Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array with the specified dtype and shape given by
    ``shape + (alpha.shape[-1],)`` if ``shape`` is not None, or else
    ``alpha.shape``.
  """
  key, _ = _check_prng_key("dirichlet", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `dirichlet` must be a float "
                     f"dtype, got {dtype}")
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "dirichlet", shape)
  return maybe_auto_axes(_dirichlet, out_sharding,
                         shape=shape, dtype=dtype)(key, alpha)

