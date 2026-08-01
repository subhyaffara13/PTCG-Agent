
def _lsa_body(current_row, val):
  """Main loop in the Hungarian algorithm."""
  costs, u, v, path, row4col, col4row = val

  sink, min_value, sr, sc, shortest_path_costs, path = _find_augmenting_path(
      costs, u, v, path, row4col, current_row
  )

  u = u.at[current_row].add(min_value)

  mask = sr & (jnp.arange(costs.shape[0]) != current_row)
  u = jnp.where(mask, u + min_value - shortest_path_costs[col4row], u)

  v = jnp.where(sc, v + shortest_path_costs - min_value, v)

  def augment(carry):
    sink, row4col, col4row, _ = carry
    i = path[sink]
    row4col = row4col.at[sink].set(i)
    col4row, sink = col4row.at[i].set(sink), col4row[i]
    breakvar = i == current_row
    return sink, row4col, col4row, breakvar

  _, row4col, col4row, _ = jax.lax.while_loop(
      lambda val: ~val[-1], augment, (sink, row4col, col4row, False)
  )

  return costs, u, v, path, row4col, col4row

