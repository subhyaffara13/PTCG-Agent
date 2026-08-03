import math


def reduce_reduce_expression(
    expr: Reduce, assignments: dict[Variable, Constant]
) -> Expression | Unsatisfiable:
  reduced_expr = reduce_expression(expr.expression, assignments)

  def default():
    """We don't know how to reduce further."""
    assert not isinstance(reduced_expr, Unsatisfiable)
    return dataclasses.replace(expr, expression=reduced_expr)

  match reduced_expr:
    case Unsatisfiable():
      return Unsatisfiable()
    case RegisterLayout(value=fa.TiledLayout() as layout):
      # TODO(allanrenucci): Add support for reducing tiled layouts when keep_dims=True.
      if expr.keep_dims:
        return default()
      num_untiled_dims = expr.rank - len(layout.base_tile_shape)
      reduced_tiling_axes = [
          a - num_untiled_dims for a in expr.axes if a >= num_untiled_dims
      ]
      if reduced_tiling_axes:
        return RegisterLayout(layout.reduce(reduced_tiling_axes))
      return RegisterLayout(layout)
    case RegisterLayout(value=fa.WGStridedFragLayout() as layout):
      # We don't support cross-lane and non vec_size preserving reductions.
      trailing_dims = layout.shape[expr.axes[-1] + 1 :]
      if math.prod(trailing_dims) % (layout.vec_size * fa.WARPGROUP_SIZE):
        return default()
      shape = utils.reduce_shape(layout.shape, expr.axes, expr.keep_dims)
      return RegisterLayout(fa.WGStridedFragLayout(shape, layout.vec_size))
    case RegisterLayout(value=fa.WGSplatFragLayout() as layout):
      shape = utils.reduce_shape(layout.shape, expr.axes, expr.keep_dims)
      return RegisterLayout(fa.WGSplatFragLayout(shape))
    case _:
      return default()

