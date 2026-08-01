
def _memref_load_op_lowering_rule(
    ctx: LoweringContext, op: memref.LoadOp
) -> Sequence[ir.Value]:
  """Lowering rule for memref.LoadOp.

  Loads are never transformed so this rule is mostly just a pass-through.
  """
  del ctx

  in_transforms = inference_utils.in_transforms(op)[0]
  if in_transforms:
    raise NotImplementedError(f"memref.LoadOp does not support transforms: {op}")

  new_load_op = memref.LoadOp(
      memref=unwrap_transformed_memref(op.memref, in_transforms),
      indices=op.indices,
      nontemporal=op.nontemporal,
  )
  return [new_load_op.result]

