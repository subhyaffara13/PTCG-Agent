
def _get_cluster_ref_op_lowering_rule(
    _: LoweringContext, op: mgpu.GetClusterRefOp,
) -> Sequence[ir.Value]:
  index = ir.IndexType.get()
  specified_idxs = [
      (d, dim) for d, dim in zip((op.x, op.y, op.z), gpu.Dimension)
      if d is not None
  ]
  if len(specified_idxs) != 1:
    raise ValueError(
        "Exactly one cluster dimension must be specified, got"
        f" {len(specified_idxs)}"
    )
  [(idx, dim)] = specified_idxs
  [in_transforms] = inference_utils.in_transforms(op)
  result = utils.get_cluster_ref(
      unwrap_transformed_memref(op.source, in_transforms),
      dim,
      arith.index_cast(index, idx),
      generic=False,
  )
  [out_transforms] = inference_utils.out_transforms(op)
  return [wrap_transformed_memref(result, op.result.type, out_transforms)]

