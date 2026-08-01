
def num_programs(axis: int) -> int | jax_typing.Array:
  """Returns the size of the grid along the given axis."""
  return num_programs_p.bind(axis=axis)

