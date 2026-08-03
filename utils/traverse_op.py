from typing import Callable

def traverse_op(
    op: ir.OpView,
    callback: Callable[[ir.OpView], None],
):
  """Traverses the operation and applies the callback in pre-order fashion.

  Skips recursing into `mgpu.CustomPrimitiveOp`s, and assumes that the values
  iterated on are not being modified.
  """
  callback(op)
  # The block of a mosaic_gpu.custom_primitive op is already lowered so it
  # should not be traversed.
  if not isinstance(op, mgpu.CustomPrimitiveOp):
    for region in op.operation.regions:
      for block in region:
        for block_op in block.operations:
          traverse_op(block_op, callback)

