
def _get_grid_bounds(grid_mapping: pallas_core.GridMapping) -> tuple[int, ...]:
  if grid_mapping.num_dynamic_grid_bounds > 0:
    raise NotImplementedError(
        "Dynamic grid bounds not (yet) supported in GPU interpret mode."
    )
  result = []
  for x in grid_mapping.grid:
    # We have already tested for the absence of dynamic grid bounds. So all
    # entries in the grid should be ints.
    assert isinstance(x, int)
    result.append(x)
  return tuple(result)

