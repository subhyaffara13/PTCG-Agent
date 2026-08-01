
def _replace_uses_in_block(old: ir.Value, new: ir.Value, block: ir.Block):
  """Replaces all uses of the `old` value with the `new` value in `block`."""

  def is_contained_within_block(operand: ir.OpOperand, block: ir.Block) -> bool:
    current_op = operand.owner.operation
    while (parent := current_op.parent) is not None:
      if current_op.block == block:
        return True
      current_op = parent
    return False

  for use in old.uses:
    if is_contained_within_block(use, block):
      use.owner.operands[use.operand_number] = new

