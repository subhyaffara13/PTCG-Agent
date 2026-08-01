
def _get_index_mapping(avals) -> dict[int, tuple[int, ...]]:
  indices = {}
  counter = 0
  for i, in_aval in enumerate(avals):
    local_counter = []
    for _ in range(len(in_aval.lo_ty())):
      local_counter.append(counter)
      counter += 1
    indices[i] = tuple(local_counter)
  return indices

