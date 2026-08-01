
def _logpdf(x: Array, alpha: Array) -> Array:
  if alpha.ndim != 1:
    raise ValueError(
      f"`alpha` must be one-dimensional; got alpha.shape={alpha.shape}"
    )
  if x.shape[0] not in (alpha.shape[0], alpha.shape[0] - 1):
    raise ValueError(
      "`x` must have either the same number of entries as `alpha` "
      f"or one entry fewer; got x.shape={x.shape}, alpha.shape={alpha.shape}"
    )
  one = _lax_const(x, 1)
  if x.shape[0] != alpha.shape[0]:
    x = jnp.concatenate([x, lax.sub(one, x.sum(0, keepdims=True))], axis=0)
  normalize_term = jnp.sum(gammaln(alpha)) - gammaln(jnp.sum(alpha))
  if x.ndim > 1:
    alpha = lax.broadcast_in_dim(alpha, alpha.shape + (1,) * (x.ndim - 1), (0,))
  log_probs = lax.sub(jnp.sum(xlogy(lax.sub(alpha, one), x), axis=0), normalize_term)
  return jnp.where(_is_simplex(x), log_probs, -np.inf)

