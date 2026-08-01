
def _multivariate_normal(key, mean, cov, shape, dtype, method) -> Array:
  if not np.ndim(mean) >= 1:
    msg = "multivariate_normal requires mean.ndim >= 1, got mean.ndim == {}"
    raise ValueError(msg.format(np.ndim(mean)))
  if not np.ndim(cov) >= 2:
    msg = "multivariate_normal requires cov.ndim >= 2, got cov.ndim == {}"
    raise ValueError(msg.format(np.ndim(cov)))
  n = mean.shape[-1]
  if np.shape(cov)[-2:] != (n, n):
    msg = ("multivariate_normal requires cov.shape == (..., n, n) for n={n}, "
           "but got cov.shape == {shape}.")
    raise ValueError(msg.format(n=n, shape=np.shape(cov)))

  if shape is None:
    shape = lax.broadcast_shapes(mean.shape[:-1], cov.shape[:-2])
  else:
    _check_shape("normal", shape, mean.shape[:-1], cov.shape[:-2])

  if method == 'svd':
    (u, s, _) = jnp_linalg.svd(cov)
    factor = u * jnp.sqrt(s[..., None, :])
  elif method == 'eigh':
    (w, v) = jnp_linalg.eigh(cov)
    factor = v * jnp.sqrt(w[..., None, :])
  else: # 'cholesky'
    factor = jnp_linalg.cholesky(cov)
  normal_samples = normal(key, shape + mean.shape[-1:], dtype)
  with config.numpy_rank_promotion('allow'):
    result = mean + jnp_einsum.einsum('...ij,...j->...i', factor, normal_samples)
  return result

