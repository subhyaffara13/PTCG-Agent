
def _binomial(n, k):
    return binomial(n, k, evaluate=False)


def _binomial(key, count, prob, shape, dtype) -> Array:
  # The implementation matches TensorFlow and TensorFlow Probability:
  # https://github.com/tensorflow/tensorflow/blob/v2.2.0-rc3/tensorflow/core/kernels/random_binomial_op.cc
  # and tensorflow_probability.substrates.jax.distributions.Binomial
  # For n * p < 10, we use the binomial inverse algorithm; otherwise btrs.
  if shape is None:
    shape = jnp.broadcast_shapes(np.shape(count), np.shape(prob))
  else:
    _check_shape("binomial", shape, np.shape(count), np.shape(prob))
  (prob,) = promote_dtypes_inexact(prob)
  count = lax.convert_element_type(count, prob.dtype)
  count = jnp.broadcast_to(count, shape)
  prob = jnp.broadcast_to(prob, shape)
  p_lt_half = prob < 0.5
  q = lax.select(p_lt_half, prob, 1.0 - prob)
  count_nan_or_neg = _isnan(count) | (count < 0.0)
  count_inf = jnp.isinf(count)
  q_is_nan = _isnan(q)
  q_l_0 = q < 0.0
  q = lax.select(q_is_nan | q_l_0, lax.full_like(q, 0.01), q)
  use_inversion = count_nan_or_neg | (count * q <= 10.0)

  # consistent with np.random.binomial behavior for float count input
  count = jnp.floor(count)

  count_inv = lax.select(use_inversion, count, lax.full_like(count, 0.0))
  count_btrs = lax.select(use_inversion, lax.full_like(count, 1e4), count)
  q_btrs = lax.select(use_inversion, lax.full_like(q, 0.5), q)
  max_iters = dtype.type(dtypes.finfo(dtype).max)
  samples = lax.select(
    use_inversion,
    _binomial_inversion(key, count_inv, q, shape, dtype, max_iters),
    _btrs(key, count_btrs, q_btrs, shape, dtype, max_iters),
  )
  # ensure nan q always leads to nan output and nan or neg count leads to nan
  # as discussed in https://github.com/jax-ml/jax/pull/16134#pullrequestreview-1446642709
  invalid = (q_l_0 | q_is_nan | count_nan_or_neg)
  samples = lax.select(
    invalid,
    jnp.full_like(samples, np.nan, dtype),
    samples,
  )

  # +inf count leads to inf
  samples = lax.select(
    count_inf & (~invalid),
    jnp.full_like(samples, np.inf, dtype),
    samples,
  )

  samples = lax.select(
    p_lt_half | count_nan_or_neg | q_is_nan | count_inf,
    samples,
    count.astype(dtype) - samples,
  )
  return samples

