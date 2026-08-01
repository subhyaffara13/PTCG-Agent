
def reduce_constraint(
    constraint: Constraint, assignments: dict[Variable, Constant]
) -> Constraint | Unsatisfiable:
  """Reduces a constraint."""

  match constraint:
    case Equals(lhs=lhs, rhs=rhs):
      lhs_red = reduce_expression(lhs, assignments)
      if isinstance(lhs_red, Unsatisfiable):
        return Unsatisfiable()
      rhs_red = reduce_expression(rhs, assignments)
      if isinstance(rhs_red, Unsatisfiable):
        return Unsatisfiable()
      return Equals(lhs_red, rhs_red).canonicalize()
    case Relayout(source=source, target=target) as relayout:
      source_red = reduce_expression(source, assignments)
      target_red = reduce_expression(target, assignments)
      if isinstance(source_red, Unsatisfiable) or isinstance(
          target_red, Unsatisfiable
      ):
        return Unsatisfiable()
      reduced = dataclasses.replace(
          relayout, source=source_red, target=target_red
      )
      return reduced.canonicalize()
    case NotOfType(expr=expr, type=ty):
      expr_red = reduce_expression(expr, assignments)
      if isinstance(expr_red, Unsatisfiable):
        return Unsatisfiable()
      return NotOfType(expr_red, ty)
    case IsTransferable(source=source, target=target) as transfer:
      source_red = reduce_expression(source, assignments)
      target_red = reduce_expression(target, assignments)
      if isinstance(source_red, Unsatisfiable) or isinstance(target_red, Unsatisfiable):
        return Unsatisfiable()
      return dataclasses.replace(transfer, source=source_red, target=target_red)
    case IsValidMmaTiling(expr=expr) as is_valid_mma_tiling:
      expr_red = reduce_expression(expr, assignments)
      if isinstance(expr_red, Unsatisfiable):
        return Unsatisfiable()
      return dataclasses.replace(is_valid_mma_tiling, expr=expr_red)
    case Divides(expr=expr, tiling_multiple=tiling_multiple):
      expr_red = reduce_expression(expr, assignments)
      if isinstance(expr_red, Unsatisfiable):
        return Unsatisfiable()
      return Divides(expr_red, tiling_multiple)
    case MinorDimDivisibleBy(expr=expr, divisor=divisor):
      expr_red = reduce_expression(expr, assignments)
      if isinstance(expr_red, Unsatisfiable):
        return Unsatisfiable()
      return MinorDimDivisibleBy(expr_red, divisor)
    case IsSupportedBroadcast(src=src, dst=dst, dims=dims):
      src_red = reduce_expression(src, assignments)
      dst_red = reduce_expression(dst, assignments)
      if isinstance(src_red, Unsatisfiable) or isinstance(
          dst_red, Unsatisfiable
      ):
        return Unsatisfiable()
      return IsSupportedBroadcast(src_red, dst_red, dims)
    case AlwaysTrue():
      return constraint
    case _ as never:
      assert_never(never)

