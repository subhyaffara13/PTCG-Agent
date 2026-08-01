
def _unravel_program_id(
    block_id: ir.Value,
    axis: int,
    dimensions: tuple[int, ...],
    row_major: bool = False
) -> ir.Value:
  """Computes the program ID for axes compressed into one block dimension."""
  if row_major:
    div_value = math.prod(dimensions[axis+1:])
  else:
    div_value = math.prod(dimensions[:axis])
  div_value = _as_index(_i32_constant(div_value))
  pid = arith_dialect.divui(block_id, div_value)
  axis_size = _as_index(_i32_constant(dimensions[axis]))
  pid = arith_dialect.remui(pid, axis_size)
  return arith_dialect.index_cast(ir.IntegerType.get_signless(32), pid)

