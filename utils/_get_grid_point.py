
def _get_grid_point(
    loop_indices: tuple[Array, ...],
    grid_point_coordinates: _GridPointCoordinatesPerDim,
) -> Array:
  """Indexes each entry in `grid_point_coordinates` with the corresponding entry in `loop_indices`.

  If an entry in `grid_point_coordinates` is an empty array, the corresponding
  entry in the returned array is the corresponding entry in `loop_indices`.
  Otherwise, the returned array contains the entry in `grid_point_coordinates`
  indexed with the corresponding entry in `loop_indices`.

  Args:
    loop_indices: A tuple of loop indices.
    grid_point_coordinates: A tuple of coordinate arrays for each dimension in
      the grid. Dimensions with 'arbitrary' semantics are represented by empty
      arrays. Dimensions with 'parallel' semantics are represented by arrays of
      randomized coordinates.

  Returns:
    A 1-dimensional array containing the coordinates for the grid point
    corresponding to the specified `loop_indices`.
  """
  grid_point = []
  for li, coords in zip(loop_indices, grid_point_coordinates):
    grid_point.append(li if jnp.size(coords) == 0 else coords[li])
  return jnp.array(grid_point, dtype=np.int32)

