
def _program_id(
    parallel_axis: int, squashed_dims: tuple[int, ...], grid_size: int
) -> ir.Value:
  """Returns the id of the current kernel instance along the given axis in the original Pallas grid."""
  if parallel_axis < len(squashed_dims):
    # All squashed dimensions are mapped to Dimension.z.
    block_id = gpu_dialect.block_id(gpu_dialect.Dimension.z)
    idx = len(squashed_dims) - 1 - parallel_axis
    return _unravel_program_id(block_id, idx, squashed_dims)
  else:
    idx = grid_size - 1 - parallel_axis
    assert idx in (0, 1, 2)
    return arith_dialect.index_cast(
        ir.IntegerType.get_signless(32),
        gpu_dialect.block_id(gpu_dialect.Dimension(idx)))


def _program_id(axis: int, launch_grid: Sequence[int]) -> ir.Value:
  if axis not in range(3):
    raise ValueError(f"axis must be in [0, 3), but got: {axis}")
  if launch_grid[axis] == 1:
    return _i32_constant(0)
  return tt_dialect.get_program_id(axis)

