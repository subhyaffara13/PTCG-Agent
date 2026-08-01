
def _memref_cast_op_lowering_rule(
    ctx: LoweringContext, op: memref.CastOp
) -> Sequence[ir.Value]:
  del ctx
  in_ty = ir.MemRefType(op.source.type)
  out_ty = ir.MemRefType(op.result.type)
  in_strides, _ = in_ty.get_strides_and_offset()
  out_strides, _ = out_ty.get_strides_and_offset()

  unoffseted_in_ty = ir.MemRefType.get(
      in_ty.shape,
      in_ty.element_type,
      memory_space=in_ty.memory_space,
      layout=ir.StridedLayoutAttr.get(0, in_strides),
  )
  unoffseted_out_ty = ir.MemRefType.get(
      out_ty.shape,
      out_ty.element_type,
      memory_space=out_ty.memory_space,
      layout=ir.StridedLayoutAttr.get(0, out_strides),
  )

  if unoffseted_in_ty != unoffseted_out_ty:
    raise NotImplementedError(
        "Only support memref.cast where the input and output types are the "
        f"same up to offset, but got {in_ty=} and {out_ty=}."
    )

  memory_space = ir.MemRefType(op.result.type).memory_space
  if memory_space == utils.smem():
    [in_transforms] = inference_utils.in_transforms(op)
    [out_transforms] = inference_utils.out_transforms(op)
    if in_transforms != out_transforms:
      raise NotImplementedError(
          "memref.cast transforms must have identical transforms for both "
          f"input and output but got {in_transforms=} and {out_transforms=}"
      )
    result = memref.cast(
        transform_type(ir.MemRefType(op.result.type), out_transforms),
        unwrap_transformed_memref(op.source, in_transforms),
    )
    return [wrap_transformed_memref(result, op.result.type, out_transforms)]

  if memory_space == utils.tmem():
    [in_tmem_layout] = inference_utils.in_tmem_layouts(op)
    [out_tmem_layout] = inference_utils.out_tmem_layouts(op)
    if in_tmem_layout != out_tmem_layout:
      raise NotImplementedError(
          "memref.cast tmem layouts must be identical for both input and"
          f" output but got {in_tmem_layout=} and {out_tmem_layout=}"
      )
    return [_tmem_ref_to_ir(_tmem_ref_from_ir(op.source, in_tmem_layout),
                            op.result.type)]

  raise NotImplementedError(
      f"Unsupported memory space when lowering memref.cast: {memory_space}"
  )

