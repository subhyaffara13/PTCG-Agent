
def _find_short_augpath_while_body(val):
  """Main loop to find augmenting path."""
  (
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
  ) = val

  index = -1
  lowest = jnp.inf
  sr = sr.at[current_row].set(True)

  init = (
      remaining,
      min_value,
      costs,
      current_row,
      u,
      v,
      shortest_path_costs,
      path,
      lowest,
      row4col,
      index,
  )
  output = jax.lax.fori_loop(
      0, num_remaining, _find_short_augpath_while_body_inner_for, init
  )
  (
      remaining,
      _,
      costs,
      current_row,
      u,
      v,
      shortest_path_costs,
      path,
      lowest,
      row4col,
      index,
  ) = output

  min_value = lowest
  # infeasible costs matrix
  sink = jnp.where(min_value == jnp.inf, -1, sink)

  state = remaining, index, row4col, sink, current_row, sc, num_remaining
  (remaining, sink, current_row, sc, num_remaining) = jax.tree.map(
      functools.partial(jnp.where, sink == -1),
      _find_short_augpath_while_body_tail(state),
      (remaining, sink, current_row, sc, num_remaining),
  )

  return (
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

