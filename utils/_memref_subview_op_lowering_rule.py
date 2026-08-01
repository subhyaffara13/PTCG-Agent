
def _memref_subview_op_lowering_rule(
    ctx: LoweringContext, op: memref.SubViewOp
) -> Sequence[ir.Value]:
  del ctx

  if any(s != 1 for s in op.static_strides):
    raise NotImplementedError("SubViewOp only supports static strides of 1.")
  if op.sizes:
    raise NotImplementedError("SubViewOp only supports static sizes.")
  src_ty = ir.MemRefType(op.source.type)

  if utils.is_memref_transposed(src_ty):
    raise NotImplementedError("SubViewOp does not support transposed memrefs.")

  if utils.is_tmem_ref(src_ty):
    [in_tmem_layout] = inference_utils.in_tmem_layouts(op)
    [out_tmem_layout] = inference_utils.out_tmem_layouts(op)
    assert in_tmem_layout == out_tmem_layout
    ref = _tmem_ref_from_ir(op.source, in_tmem_layout)
    indices = []
    dynamic_offset_index = 0
    for offset, size in zip(op.static_offsets, op.static_sizes, strict=True):
      if ir.ShapedType.is_dynamic_size(offset):
        offset = op.offsets[dynamic_offset_index]
        dynamic_offset_index += 1
      indices.append(utils.DynamicSlice(offset, size))
    return [_tmem_ref_to_ir(ref.slice(*indices), op.result.type)]

  in_transforms = inference_utils.in_transforms(op)[0]
  out_transforms = inference_utils.out_transforms(op)[0]

  if in_transforms != out_transforms:
    raise NotImplementedError(
        "SubViewOp transforms for the input and output refs must be identical."
    )

  swizzle = swizzle_from_transforms_attr(out_transforms)
  if swizzle != mgpu.SwizzlingMode.kNoSwizzle:
    swizzle_elems = swizzle * 8 // utils.bitwidth(src_ty.element_type)
    source_strides, _ = src_ty.get_strides_and_offset()
    dyn_offset_index = 0
    for stride, static_offset, size in zip(
        source_strides, op.static_offsets, op.static_sizes, strict=True
    ):
      offset: int | ir.Value
      if ir.ShapedType.is_dynamic_size(static_offset):
        offset = op.offsets[dyn_offset_index]
        dyn_offset_index += 1
      else:
        offset = static_offset
      if stride != 1:
        continue
      # A dimension with stride 1 is a minor dimension and is swizzled.
      if size % swizzle_elems != 0:
        raise ValueError(
            f"Swizzled dimension of {size=} is not a multiple of"
            f" {swizzle_elems=}."
        )
      if isinstance(offset, ir.Value):
        if not utils.is_known_divisible(offset, swizzle_elems):
          raise ValueError(
              "subview dynamic offset is not a known multiple of"
              f" {swizzle_elems=}."
          )
      elif offset % swizzle_elems != 0:
        raise ValueError(
            f"subview {offset=} is not a multiple of {swizzle_elems=}."
        )

  unwrapped_source_ref = unwrap_transformed_memref(op.source, in_transforms)
  transforms = memref_transforms_from_transforms_attr(out_transforms)
  match transforms:
    case ():
      new_subview_op = memref.SubViewOp(
          op.result.type,
          unwrapped_source_ref,
          op.offsets,
          sizes=[],
          strides=[],
          static_offsets=op.static_offsets,
          static_sizes=op.static_sizes,
          static_strides=op.static_strides,
      )
    case (lc.TileTransform() as tile_transform, ):
      in_transformed_ty = ir.MemRefType(unwrapped_source_ref.type)
      tiling = tile_transform.tiling
      if any(
          ir.ShapedType.is_dynamic_size(s)
          for s in list(op.static_sizes)[-len(tiling) :]
      ):
        raise NotImplementedError(
            "SubViewOp only supports static sizes for the tiled dimensions."
        )
      new_sizes = tile_transform.transform_shape(list(op.static_sizes))
      # TODO(bchetioui): support transposed offsets.
      new_static_offsets, new_dynamic_offsets = _tile_transform_offsets(
          tiling, list(op.static_offsets), list(op.offsets)
      )

      new_subview_op = memref.SubViewOp(
          transform_type(ir.MemRefType(op.result.type), transforms),
          unwrapped_source_ref,
          new_dynamic_offsets,
          sizes=[],
          strides=[],
          static_offsets=new_static_offsets,
          static_sizes=new_sizes,
          static_strides=[1] * len(in_transformed_ty.shape),
      )
    case _:
      raise NotImplementedError(
          "SubViewOp only supports a single tile transform."
      )

  wrapped_ref = wrap_transformed_memref(
      new_subview_op.result, op.result.type, out_transforms
  )
  return [wrapped_ref]

