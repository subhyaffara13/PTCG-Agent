
def _partition_by_player(val, p_vec, num_players):
  """Partitions a value by the players vector."""
  parts = []
  for p in range(num_players):
    inds = p_vec == p
    if inds.size > 0:
      parts.append(val[inds])
    else:
      parts.append(None)
  return parts

