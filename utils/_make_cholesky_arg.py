
def _make_cholesky_arg(shape, dtype, rng):
  a = jtu.rand_default(rng)(shape, dtype)
  return np.matmul(a, jnp.conj(np.swapaxes(a, -1, -2)))

