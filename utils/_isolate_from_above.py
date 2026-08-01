
def _isolate_from_above(
    op: ir.Operation | ir.OpView
) -> ir.Operation | ir.OpView:
  """Makes `op` conform to the `IsolatedFromAbove` trait.

  This replaces all captured values with new op operands.
  """
  if len(op.regions) != 1:
    raise NotImplementedError("Only support ops with one region.")
  if len(op.regions[0].blocks) != 1:
    raise NotImplementedError("Only support ops with one block.")

  block = op.regions[0].blocks[0]
  captures = _closed_over_values(block)
  if not captures:
    return op

  # 1. Create the new operation shell with the expanded operands.
  new_op = ir.Operation.create(
      name=op.name,
      results=[res.type for res in op.results],
      operands=list(op.operands) + captures,
      attributes=dict(op.attributes),
      regions=1,
  )

  # 2. Move the block from the old op to the new op.
  block.append_to(new_op.regions[0])

  # 3. Create new block arguments for the captured values.
  new_args = []
  for capture in captures:
    new_args.append(block.add_argument(capture.type, capture.location))

  # 4. Redirect all references from captured values to the newly created
  # block's arguments.
  for capture, new_arg in zip(captures, block.arguments[-len(captures) :]):
    _replace_uses_in_block(capture, new_arg, block)

  # 5. Clean up the now-empty old operation.
  op.erase()

  return new_op

