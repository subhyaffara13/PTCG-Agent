
def _poisson(key, lam, shape, dtype) -> Array:
  # The implementation matches TensorFlow and NumPy:
  # https://github.com/tensorflow/tensorflow/blob/v2.2.0-rc3/tensorflow/core/kernels/random_poisson_op.cc
  # https://github.com/numpy/numpy/blob/v1.18.3/numpy/random/src/distributions/distributions.c#L574
  # For lambda < 10, we use the Knuth algorithm; otherwise, we use transformed
  # rejection sampling.
  use_knuth = _isnan(lam) | (lam < 10)
  lam_knuth = lax.select(use_knuth, lam, lax.full_like(lam, 0.0))
  # The acceptance probability for rejection sampling maxes out at 89% as
  # λ -> ∞, so pick some arbitrary large value.
  lam_rejection = lax.select(use_knuth, lax.full_like(lam, 1e5), lam)
  max_iters = dtype.type(dtypes.iinfo(dtype).max)  # insanely conservative
  result = lax.select(
    use_knuth,
    _poisson_knuth(key, lam_knuth, shape, dtype, max_iters),
    _poisson_rejection(key, lam_rejection, shape, dtype, max_iters),
  )
  return lax.select(lam == 0, jnp.zeros_like(result), result)

