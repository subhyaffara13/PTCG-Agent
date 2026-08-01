
def _get_parallel_subgrid_size(
    parallel_semantics_per_dim: tuple[bool, ...], grid: tuple[int, ...]
) -> int:
  """Returns the size of the subgrid along the parallel dimensions."""
  return math.prod(
      dim_size if parallel_dim else 1
      for dim_size, parallel_dim in zip(grid, parallel_semantics_per_dim)
  )

