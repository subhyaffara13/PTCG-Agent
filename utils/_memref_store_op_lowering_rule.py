
def _memref_store_op_lowering_rule(
    ctx: LoweringContext, op: memref.StoreOp
) -> Sequence[ir.Value]:
  """Lowering rule for memref.StoreOp.

  Stores are never transformed so this rule is mostly just a pass-through.
  """
  del ctx

  in_transforms = inference_utils.in_transforms(op)[0]
  if in_transforms:
    raise NotImplementedError(f"memref.StoreOp does not support transforms: {op}")

  memref.StoreOp(
      value=op.value,
      memref=unwrap_transformed_memref(op.memref, in_transforms),
      indices=op.indices,
      nontemporal=op.nontemporal,
  )
  return []

