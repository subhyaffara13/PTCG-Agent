
def _is_index_invariant(
    spec: pallas_core.BlockSpec, grid: pallas_core.TupleGrid
) -> bool:
  if (index_map := spec.index_map) is None:
    return True
  return not any(_uses_arguments(index_map, len(grid)))

