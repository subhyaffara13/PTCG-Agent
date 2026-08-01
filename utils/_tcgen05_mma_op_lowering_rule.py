
def _tcgen05_mma_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.TcGen05MMAOp
) -> Sequence[ir.Value]:
  ctx.check_collective(op)

  def tmem_layout(operand):
    result = inference_utils.in_tmem_layout_for_operand(op, operand)
    # satisfy the type checker
    assert result is not None
    return result

  acc_ref = _tmem_ref_from_ir(op.accumulator, tmem_layout(op.accumulator))

  if op.a_sparse_metadata is not None:
    a_sparse_metadata = _tmem_ref_from_ir(
        op.a_sparse_metadata, tmem_layout(op.a_sparse_metadata)
    )
  else:
    a_sparse_metadata = None
  if (scaled := op.a_scale is not None) != (op.b_scale is not None):
    raise ValueError("Expected both or neither of scales to be specified.")
  if scaled:
    a_scale = _tmem_ref_from_ir(op.a_scale, tmem_layout(op.a_scale))  # pyrefly: ignore[bad-argument-type]
    b_scale = _tmem_ref_from_ir(op.b_scale, tmem_layout(op.b_scale))  # pyrefly: ignore[bad-argument-type]
  else:
    a_scale = None
    b_scale = None

  if utils.is_smem_ref(op.a):
    a_transforms, b_transforms = inference_utils.in_transforms(op)
    a_swizzle = swizzle_from_transforms_attr(a_transforms)
    b_swizzle = swizzle_from_transforms_attr(b_transforms)
    a_ref = unwrap_transformed_memref(op.a, a_transforms)
    b_ref = unwrap_transformed_memref(op.b, b_transforms)
  else:
    a_ref = _tmem_ref_from_ir(op.a, tmem_layout(op.a))
    [b_transforms] = inference_utils.in_transforms(op)
    b_swizzle = swizzle_from_transforms_attr(b_transforms)
    a_swizzle = b_swizzle
    b_ref = unwrap_transformed_memref(op.b, b_transforms)

  with utils.when(ctx.single_lane_predicate):
    tcgen05.mma(
        acc_ref,
        a_ref,
        b_ref,
        a_swizzle=a_swizzle,
        b_swizzle=b_swizzle,
        a_scale=a_scale,
        b_scale=b_scale,
        accumulate=op.accumulate,
        collective=op.collective.value,
        a_sparse_metadata=a_sparse_metadata,
    )

  return []

