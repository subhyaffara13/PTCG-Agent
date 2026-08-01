
def _get_parallel_dim_semantics(
    mosaic_params: mosaic_core.CompilerParams, num_dimensions_in_grid: int,
) -> tuple[bool, ...]:
  """Returns a tuple indicating which grid dimensions have parallel semantics.

  Args:
    mosaic_params: The compiler params for the Mosaic TPU backend.
    num_dimensions_in_grid: The number of dimensions in the grid.

  Returns:
    A tuple of booleans where the entry at index `i` is `True` precisely if the
    `i`-th dimension in the grid has parallel semantics.

  Raises:
    ValueError: If the dimensions with parallel semantics do not form a prefix
      of the grid.
  """
  if mosaic_params.dimension_semantics is None:
    return (False,) * num_dimensions_in_grid
  result = tuple(ds in ('parallel', mosaic_core.PARALLEL)
                 for ds in mosaic_params.dimension_semantics)
  for ds0, ds1 in zip(result[:-1], result[1:]):
    if ds1 and not ds0:
      raise ValueError(
          'Dimensions with parallel semantics must form a prefix of the grid.'
      )
  return result

