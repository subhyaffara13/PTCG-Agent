
def _tp_inner_spec(
    shape: list[int], axis_name: str, axis_size: int
) -> list[str | None]:
  """Inner-dim (last-axis) partition spec; falls back to fully replicated.

  Args:
    shape: The leaf shape.
    axis_name: Mesh axis to shard the last dim along.
    axis_size: Size of that mesh axis.

  Returns:
    A PartitionSpec-style list (axis name or None per dim).
  """
  if len(shape) < 2:
    return [None] * len(shape)
  if shape[-1] % axis_size == 0:
    return [None] * (len(shape) - 1) + [axis_name]
  return [None] * len(shape)

