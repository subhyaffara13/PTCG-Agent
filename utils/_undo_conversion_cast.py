from typing import Any

def _undo_conversion_cast(
    ir_value: ir.Value,
    expected_types: Sequence[ir.Type],
) -> tuple[builtin.UnrealizedConversionCastOp, Sequence[ir.Value]]:
  """Undoes the provided unrealized conversion cast.

  The `ir_value` must be an unrealized conversion cast. This function will
  create a new conversion cast that undoes the original one. The returned tuple
  contains:
  - The original unrealzied conversion cast (useful for extract attributes).
  - The list of operands of the original conversion cast (which are the result
    values of the undone conversion cast).

  The function will verify that the returned values have types that match
  `expected_types`.
  """
  conversion_cast: Any = ir_value.owner

  if not isinstance(conversion_cast, builtin.UnrealizedConversionCastOp):
    raise ValueError(f"{conversion_cast} is not a conversion_cast")

  cast_op = builtin.UnrealizedConversionCastOp(
      [operand.type for operand in conversion_cast.operands],
      conversion_cast.results,
  )
  converted_outputs: Sequence[ir.Value] = cast_op.results

  for v, t in zip(converted_outputs, expected_types, strict=True):
    if v.type != t:
      raise ValueError(f"Expected type {t} for value {v}")

  return conversion_cast, converted_outputs

