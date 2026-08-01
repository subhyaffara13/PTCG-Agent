
def _closed_over_values(block: ir.Block) -> list[ir.Value]:
  """Returns a list of unique values used within `block` that are defined outside of `block`."""
  def _closed_over_values_inner(
      block: ir.Block, vals_in_block: set[ir.Value]
  ) -> list[ir.Value]:
    closed_over_values = []
    for arg in block.arguments:
      vals_in_block.add(arg)
    for op in block.operations:
      for o in op.operands:
        if o not in vals_in_block:
          closed_over_values.append(o)
      for r in op.regions:
        for b in r.blocks:
          closed_over_values.extend(_closed_over_values_inner(b, vals_in_block))
      for r in op.results:
        vals_in_block.add(r)
    return closed_over_values
  result = _closed_over_values_inner(block, set())
  # Remove duplicates while preserving order.
  return list(dict.fromkeys(result))

