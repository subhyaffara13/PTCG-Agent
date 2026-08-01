
def _find_short_augpath_while_body_tail(val):
  """Post-processing to find augmenting path."""
  remaining, index, row4col, sink, i, sc, num_remaining = val

  j = remaining[index]
  pred = row4col[j] == -1
  sink = jnp.where(pred, j, sink)
  i = jnp.where(pred, i, row4col[j])

  sc = sc.at[j].set(True)
  num_remaining -= 1
  remaining = remaining.at[index].set(remaining[num_remaining])

  return remaining, sink, i, sc, num_remaining

