import copy
from typing import Any

def unzip_dynamic_grid_bounds(
    grid_spec: GridSpec) -> tuple[GridSpec, tuple[Any, ...]]:
  if dynamic_shapes_export_enabled():
    new_grid: Any = grid_spec.grid
  else:
    new_grid: Any = tuple(d if isinstance(d, int) else None for d in grid_spec.grid)
  dynamic_bounds = tuple(d for d in grid_spec.grid if not isinstance(d, int))
  # We can't use dataclasses.replace, because our fields are incompatible
  # with __init__'s signature.
  static_self = copy.copy(grid_spec)
  static_self.grid = new_grid
  return static_self, dynamic_bounds

