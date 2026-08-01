
def _projection_unit_simplex(values: jax.typing.ArrayLike) -> jax.Array:
  """Projection onto the unit simplex."""
  s = 1
  n_features = values.shape[0]  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
  u = jnp.sort(values)[::-1]
  cumsum_u = jnp.cumsum(u)
  ind = jnp.arange(n_features) + 1
  cond = s / ind + (u - cumsum_u / ind) > 0
  idx = jnp.count_nonzero(cond)
  return jax.nn.relu(s / idx + (values - cumsum_u[idx - 1] / idx))

