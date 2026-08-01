
def get_batch_size_from_per_elt_updates(
    per_elt_updates: base.Updates, per_elt_axis: int | list[int]
) -> int:
  """Get batch size from per-element updates.

  Args:
    per_elt_updates: The per-element updates.
    per_elt_axis: The axis to average over.

  Returns:
    The batch size.
  """

  def get_batch_size(u):
    if isinstance(per_elt_axis, int):
      return u.shape[per_elt_axis]
    else:
      return math.prod(u.shape[i] for i in per_elt_axis)

  batch_sizes = jax.tree.map(get_batch_size, per_elt_updates)
  batch_sizes = jax.tree.leaves(batch_sizes)
  if not all(b == batch_sizes[0] for b in batch_sizes):
    raise ValueError(
        f'Per-element updates must have the same batch size. Got: {batch_sizes}'
    )
  return batch_sizes[0]

