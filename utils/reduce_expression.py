
def reduce_expression(
    expr: Expression, assignments: dict[Variable, Constant]
) -> Expression | Unsatisfiable:
  """Reduces an expression as much as is possible given a set of known variable assignments."""
  match expr:
    case RegisterLayout() | TMEMLayout() | SMEMTransforms():
      return expr
    case Variable():
      return assignments.get(expr, expr)
    case Reduce():
      return reduce_reduce_expression(expr, assignments)
    case Reshape():
      return reduce_reshape_expression(expr, assignments)
    case Transpose():
      return reduce_transpose_expression(expr, assignments)
    case CollapseShape():
      return reduce_collapse_shape_expression(expr, assignments)
    case _:
      assert_never(expr)

