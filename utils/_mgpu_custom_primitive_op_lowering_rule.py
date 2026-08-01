
def _mgpu_custom_primitive_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.CustomPrimitiveOp
) -> Sequence[ir.Value]:
  """Lowering rule for mgpu.CustomPrimitiveOp."""
  del ctx
  block = op.body.blocks[0]
  for arg, operand in zip(block.arguments, op.operands, strict=True):
    arg.replace_all_uses_with(operand)

  return_op = None
  ip = ir.InsertionPoint.current
  for block_op in block.operations:
    if isinstance(block_op.opview, mgpu.ReturnOp):
      assert return_op is None
      return_op = block_op.opview
      continue
    block_op.detach_from_parent()
    ip.insert(block_op)

  if return_op is None:
    raise ValueError("A custom return op must terminate the block.")

  return return_op.operands

