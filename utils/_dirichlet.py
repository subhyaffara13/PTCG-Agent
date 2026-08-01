
def _dirichlet(key, alpha, shape, dtype) -> Array:
  from jax._src.nn.functions import softmax  # pyrefly: ignore[missing-import]

  if not np.ndim(alpha) >= 1:
    msg = "dirichlet requires alpha.ndim >= 1, got alpha.ndim == {}"
    raise ValueError(msg.format(np.ndim(alpha)))

  if shape is None:
    shape = np.shape(alpha)[:-1]
  else:
    _check_shape("dirichlet", shape, np.shape(alpha)[:-1])

  alpha = lax.convert_element_type(alpha, dtype)

  # Compute gamma in log space, otherwise small alpha can lead to poor behavior.
  log_gamma_samples = loggamma(key, alpha, shape + np.shape(alpha)[-1:], dtype)
  return softmax(log_gamma_samples, -1)

