
def _fsdp_spec(
    shape: list[int], axis_name: str, axis_size: int
) -> list[str | None]:
  """Leading-dim FSDP partition spec; falls back to fully replicated.

  Args:
    shape: The leaf shape.
    axis_name: Mesh axis to shard the leading dim along.
    axis_size: Size of that mesh axis.

  Returns:
    A PartitionSpec-style list (axis name or None per dim).
  """
  if len(shape) < 2:
    return [None] * len(shape)
  if shape[0] % axis_size == 0:
    return [axis_name] + [None] * (len(shape) - 1)
  return [None] * len(shape)

