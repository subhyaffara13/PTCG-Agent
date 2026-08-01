
def _get_randomized_grid_coordinates(
    grid: tuple[int, ...],
    mosaic_params: mosaic_core.CompilerParams,
    random_seed: int | None,
) -> _GridPointCoordinatesPerDim:
  """Returns a tuple of randomized coordinates for each 'parallel' dimension in `grid`.

  For a dimension with 'parallel' semantics at position `d` in the grid, the
  returned tuple contains a random permutation of the sequence `[0,...,
  grid[d] - 1]` at index `d`. For each dimension with 'arbitrary' semantics,
  the resulting tuple contains an empty array. (Inserting an empty array for an
  'arbitrary' dimension at position `d` in the grid, instead of the sequence
  `[0,..., grid[d] - 1]`, allows `grid[d]` to be a dynamic value, i.e. a value
  not known at Jax trace time.)

  Args:
    grid: Tuple of sizes of the dimensions in the grid.
    mosaic_params: The compiler params for the Mosaic TPU backend.
    parallel_semantics_per_dim: A tuple of booleans indicating whether the
      corresponding dimension in the grid has parallel semantics.
    random_seed: The seed to use for randomizing coordinates in parallel
      dimensions.
  """
  parallel_semantics_per_dim = _get_parallel_dim_semantics(
      mosaic_params, len(grid)
  )

  key = jax.random.key(random_seed or 0)
  grid_point_coordinates = []
  for dim_size, parallel_dim in zip(grid, parallel_semantics_per_dim):
    if parallel_dim:
      # The size of a dimension with `parallel` semantics must be known at Jax
      # trace time. This ensures that the arguments to `jnp.arange` and
      # `jax.random.permutation` below are valid.
      dim_size = jax_core.concrete_or_error(None, dim_size)

      coordindates_along_dim = jnp.arange(dim_size, dtype=jnp.int32)
      key, subkey = jax.random.split(key)
      coordindates_along_dim = jax.random.permutation(
          subkey, coordindates_along_dim
      )
      grid_point_coordinates.append(coordindates_along_dim)
    else:
      grid_point_coordinates.append(jnp.array((), dtype=jnp.int32))

  return tuple(grid_point_coordinates)

