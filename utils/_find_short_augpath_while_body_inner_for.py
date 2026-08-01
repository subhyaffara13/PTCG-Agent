
def _find_short_augpath_while_body_inner_for(it, val):
  """Inner loop of the main loop to find augmenting path."""
  (
      remaining,
      min_value,
      costs,
      i,
      u,
      v,
      shortest_path_costs,
      path,
      lowest,
      row4col,
      index,
  ) = val

  j = remaining[it]

  r = min_value + costs[i, j] - u[i] - v[j]

  path = path.at[j].set(jnp.where(r < shortest_path_costs[j], i, path[j]))

  shortest_path_costs = shortest_path_costs.at[j].min(r)

  index = jnp.where(
      (shortest_path_costs[j] < lowest)
      | ((shortest_path_costs[j] == lowest) & (row4col[j] == -1)),
      it,
      index,
  )

  lowest = jnp.minimum(lowest, shortest_path_costs[j])

  return (
      remaining,
      min_value,
      costs,
      i,
      u,
      v,
      shortest_path_costs,
      path,
      lowest,
      row4col,
      index,
  )

