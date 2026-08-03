import math


def _get_grid_and_cluster_dims_and_num_threads(
    grid_mapping: pallas_core.GridMapping, mesh: plgpu.Mesh | None
) -> tuple[tuple[int, ...], tuple[int, ...], int]:
  if not mesh:
    num_threads = 1
    cluster_dims = ()
    grid_dims = _get_grid_bounds(grid_mapping)
  elif isinstance(mesh, plgpu.Mesh):
    num_threads = int(mesh.num_threads or 1)
    cluster_dims = tuple(mesh.cluster) if mesh.cluster is not None else ()
    grid_dims = tuple(mesh.grid)
  else:
    raise ValueError(f"Unsupported mesh type: {type(mesh)}")

  reconstructed_grid = grid_dims + cluster_dims + (num_threads,)
  if math.prod(_get_grid_bounds(grid_mapping)) != math.prod(reconstructed_grid):
    raise NotImplementedError(
        f"Invalid grid {grid_mapping.grid} in grid_mapping: expected grid to"
        f" have the same size as {reconstructed_grid}"
    )

  return grid_dims, cluster_dims, num_threads

