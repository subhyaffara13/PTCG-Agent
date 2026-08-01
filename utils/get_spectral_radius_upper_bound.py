
def get_spectral_radius_upper_bound(matrix):
  # Get an upper bound on the spectral radius of a matrix.
  a = jnp.linalg.matrix_norm(matrix, ord='fro')
  # TODO(rdyro): https://github.com/jax-ml/jax/issues/26555
  b = jnp.linalg.matrix_norm(matrix, ord=1) if matrix.size != 0 else 0
  return jnp.minimum(a, b)

