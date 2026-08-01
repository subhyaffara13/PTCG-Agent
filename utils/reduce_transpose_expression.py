
def reduce_transpose_expression(
    transpose: Transpose, assignments: dict[Variable, Constant]
) -> Expression | Unsatisfiable:
  reduced_expr = reduce_expression(transpose.expression, assignments)
  match reduced_expr:
    case Unsatisfiable():
      return Unsatisfiable()
    case SMEMTransforms(tiling=tile_transform):
      if tile_transform is None:
        return SMEMTransforms(None)
      tiling = tile_transform.tiling
      permutation = transpose.permutation
      tiling_offset = len(permutation) - len(tiling)
      # We reject if there's a swap between tiled dimensions and untiled dimensions.
      #
      # For example:
      #   A permutation (0, 3, 2, 1) and tiling of length <=2, we reject because tiling becomes non-contiguous.
      #   A permutation (0, 3, 2, 1) and tiling of length 3, we accept.
      if any(dim < tiling_offset for dim in permutation[-len(tiling) :]):
        return Unsatisfiable()
      new_tiling = tuple(tiling[dim - tiling_offset] for dim in permutation[-len(tiling):])
      return SMEMTransforms(lc.TileTransform(new_tiling))
    case _:
      return Transpose(expression=reduced_expr, permutation=transpose.permutation)

