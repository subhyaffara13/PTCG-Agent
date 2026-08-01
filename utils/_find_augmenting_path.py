
def _find_augmenting_path(costs, u, v, path, row4col, current_row):
  """Finds an augmenting path."""
  min_value = 0
  num_remaining = costs.shape[1]
  remaining = jnp.arange(costs.shape[1])[::-1]

  sr = jnp.zeros(costs.shape[0], bool)
  sc = jnp.zeros(costs.shape[1], bool)

  shortest_path_costs = jnp.full(costs.shape[1], jnp.inf)

  sink = -1

  init = (
      costs,
      u,
      v,
      path,
      row4col,
      current_row,
      min_value,
      num_remaining,
      remaining,
      sr,
      sc,
      shortest_path_costs,
      sink,
  )
  output = jax.lax.while_loop(
      lambda val: val[-1] == -1, _find_short_augpath_while_body, init
  )
  (
      _,
      _,
      _,
      path,
      _,
      _,
      min_value,
      _,
      _,
      sr,
      sc,
      shortest_path_costs,
      sink,
  ) = output

  return sink, min_value, sr, sc, shortest_path_costs, path

