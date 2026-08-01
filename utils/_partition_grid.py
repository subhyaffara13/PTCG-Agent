
def _partition_grid(
    grid: tuple[int | jax.Array, ...],
    core_axis: tuple[int | str, ...] | int | str | None,
    dimension_semantics: tuple[GridDimensionSemantics, ...] | None,
) -> tuple[tuple[int | jax.Array, ...], tuple[int | jax.Array, ...]]:
  if core_axis is None:
    # We aren't partitioning the grid
    return grid, (0,) * len(grid)
  if isinstance(core_axis, int):
    num_cores = num_programs(core_axis)
    core_id = program_id(core_axis)
  else:
    num_cores = jax.lax.axis_size(core_axis)
    core_id = jax.lax.axis_index(core_axis)
  # Check that num_cores is statically known
  if not isinstance(num_cores, int):
    raise NotImplementedError(
        f"Cannot partition grid over dynamic number of cores: {core_axis=}"
    )
  if num_cores == 1:
    # We aren't partitioning the grid
    return grid, (0,) * len(grid)

  # If dimension_semantics aren't provided, we assume it is all arbitrary.
  if dimension_semantics is None:
    dimension_semantics = (ARBITRARY,) * len(grid)
  if len(dimension_semantics) != len(grid):
    raise ValueError("dimension_semantics must be the same length as grid.")

  parallel_dimensions = {
      i for i, d in enumerate(dimension_semantics) if d == PARALLEL
  }
  # If there are no parallel dimensions, we can't partition the grid
  if not parallel_dimensions:
    # TODO(sharadmv): enable running kernel on just one core
    raise NotImplementedError(
        "Cannot partition over cores without parallel grid dimensions:"
        f" {dimension_semantics=}"
    )

  # Try to find a divisible dimension to partition the grid on
  divisible_dimensions = {
      i
      for i in parallel_dimensions
      if isinstance(grid[i], int) and grid[i] % num_cores == 0
  }
  if divisible_dimensions:
    first_divisible_dimension, *_ = (
        i for i in range(len(dimension_semantics)) if i in divisible_dimensions
    )
    partitioned_dim_size = grid[first_divisible_dimension] // num_cores
    partitioned_dim_offset = core_id * partitioned_dim_size
    new_grid = jax_util.tuple_update(
        grid, first_divisible_dimension, partitioned_dim_size
    )
    offsets = jax_util.tuple_update(
        (0,) * len(grid),
        first_divisible_dimension,
        partitioned_dim_offset,
    )
    return new_grid, offsets

  # Separate the remaining dimensions into dynamic and static.
  dynamic_dims = [
      i
      for i in range(len(grid))
      if i in parallel_dimensions and not isinstance(grid[i], int)
  ]
  static_dims = [
      i
      for i in range(len(grid))
      if i in parallel_dimensions and isinstance(grid[i], int)
  ]

  if len(dynamic_dims) > 1:
    raise NotImplementedError(
        f"Cannot partition over multiple dynamic parallel dimensions: {grid=}"
    )

  if dynamic_dims and not static_dims:
    # Exactly one dynamic dimension and no static non-divisible dimensions
    partition_dimension = dynamic_dims[0]
  else:
    # No divisible static dimensions, so we can't evenly partition the grid.
    # Let's pick the largest dimension and try to divide it as evenly as
    # possible.
    # TODO(sharadmv): take the product of many nondivisible dimensions to
    # potentially divide it more evenly
    largest_parallel_dimension = max(grid[i] for i in static_dims)
    partition_dimension, *_ = (
        i for i in static_dims if grid[i] == largest_parallel_dimension
    )

  base_num_iters, rem = divmod(grid[partition_dimension], num_cores)
  # We have some remainder iterations that we need to assign somewhere. We
  # know that rem < num_cores, so we can assign one extra iteration to each
  # core except for the last (num_cores - rem).
  num_iters = jnp.where(core_id < rem, base_num_iters + 1, base_num_iters)
  new_grid = jax_util.tuple_update(grid, partition_dimension, num_iters)
  # Ordinarily, we would compute the offset as:
  #   grid_offset = program_id(core_axis) * num_iters
  # However, since we have some cores that don't have an extra iteration, we
  # need to adjust the offset by `rem`.
  grid_offset = jnp.where(
      core_id < rem,
      core_id * num_iters,
      core_id * base_num_iters + rem,
  )
  offsets = jax_util.tuple_update(
      (0,) * len(grid),
      partition_dimension,
      grid_offset,
  )
  return new_grid, offsets

