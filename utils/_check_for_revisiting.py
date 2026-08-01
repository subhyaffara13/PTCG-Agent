
def _check_for_revisiting(
    token, device_id, local_core_id, loop_idx, output_blocks
):
  device_id = int(device_id)
  local_core_id = int(local_core_id)
  loop_idx = tuple(int(x) for x in loop_idx)
  try:
    output_blocks = jax.tree.map(int, output_blocks)
  except:
    raise ValueError('Advanced indexers are not supported on TPU')
  output_ranges = [
      interpret_utils.to_range(b) if b is not None else None
      for b in output_blocks
  ]

  shared_memory = _get_shared_memory()
  past_output_ranges = shared_memory.output_ranges[(device_id, local_core_id)]
  if not past_output_ranges:
    past_output_ranges.append((loop_idx, output_ranges))
    return token

  for i in range(len(output_ranges)):
    if output_ranges[i] is None:
      continue
    if past_output_ranges[-1][1][i] == output_ranges[i]:
      continue
    # TODO(jburnim): Do something constant time instead of linear here.
    past_idxs = [
        j
        for j, ors in enumerate(past_output_ranges)
        if ors[1][i] == output_ranges[i]
    ]
    if past_idxs:
      raise RuntimeError(
          f'Revisited block {output_ranges[i]} of output {i} in iteration '
          f'{loop_idx}. The block was previously visited in iterations '
          f'{past_output_ranges[past_idxs[0]][0]} through '
          f'{past_output_ranges[past_idxs[-1]][0]} .'
      )

  past_output_ranges.append((loop_idx, output_ranges))
  return token

