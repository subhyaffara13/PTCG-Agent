
def _process_grid_to_3d_grid(grid_mapping: GridMapping):
  launch_grid: list[int] = []
  launch_grid_to_pallas_grid = []

  # Preserve grid order provided to pallas_call
  for i, s in enumerate(grid_mapping.grid):
    assert isinstance(s, int)
    if i not in grid_mapping.vmapped_dims:
      launch_grid.append(s)
      launch_grid_to_pallas_grid.append(i)

  # For mapped dims, iterate from inner to outer. This follows the pallas_call
  # batching rule that prepends the vmapped dimension.
  for dim in reversed(grid_mapping.vmapped_dims):
    s = grid_mapping.grid[dim]
    assert isinstance(s, int)
    launch_grid.append(s)
    launch_grid_to_pallas_grid.append(dim)

  num_collapse = len(launch_grid[:-2])

  cuda_yz_limit = 2**16 - 1

  # Check Z and then Y launch dims to make sure they're within CUDA bounds
  if (num_collapse + 1 < len(launch_grid) and
      launch_grid[num_collapse + 1] > cuda_yz_limit):
    num_collapse += 2
  elif (num_collapse < len(launch_grid) and
        launch_grid[num_collapse] > cuda_yz_limit):
    num_collapse += 1

  collapse_dims = launch_grid[:num_collapse]
  prog_id_dims = launch_grid[num_collapse:]

  if len(collapse_dims) == 0:
    prog_ids: list[ir.Value | None] = [None] * len(prog_id_dims)
    for i in range(len(prog_id_dims)):
      prog_ids[launch_grid_to_pallas_grid[i]] = _program_id(i, prog_id_dims)

    return prog_id_dims, prog_ids

  new_grid = [math.prod(collapse_dims), *prog_id_dims]

  assert new_grid[0] < 2**31 - 1, \
          "Cannot fix pallas kernel launch grid within CUDA limits"

  out_indices: list[ir.Value | None] = [None] * len(grid_mapping.grid)

  grid0 = _program_id(0, new_grid)
  for i, s in enumerate(collapse_dims):
    out_idx = launch_grid_to_pallas_grid[i]
    s = _i32_constant(s)
    out_indices[out_idx] = _mod(grid0, s, signed=False)
    grid0 = _floordiv(grid0, s, signed=False)

  for i in range(len(prog_id_dims)):
    out_idx = launch_grid_to_pallas_grid[num_collapse + i]
    out_indices[out_idx] = _program_id(i + 1, new_grid)

  assert len(out_indices) == len(grid_mapping.grid)
  return new_grid, out_indices

