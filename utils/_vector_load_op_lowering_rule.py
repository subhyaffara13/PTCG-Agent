
def _vector_load_op_lowering_rule(
    _: LoweringContext, op: mgpu.VectorLoadOp
) -> Sequence[ir.Value]:
  out_layout_attr, = inference_utils.out_layouts(op)
  out_layout = layouts_lib.from_layout_attr(out_layout_attr)

  element_type = ir.VectorType(op.result.type).element_type
  is_signed = _default_is_signed(element_type)

  orig_ref_ty = op.source.type
  if utils.is_smem_ref(orig_ref_ty) or utils.is_cluster_smem_ref(orig_ref_ty):
    [transforms_attr] = inference_utils.in_transforms(op)
    transformed_ref = unwrap_transformed_memref(op.source, transforms_attr)
  else:
    transforms_attr = None
    transformed_ref = op.source

  def _fragmented_array_to_ir(
      fragmented_array: fa.FragmentedArray,
  ) -> ir.Value:
    return fragmented_array_to_ir(fragmented_array, op.result.type)

  if isinstance(out_layout, fa.WGStridedFragLayout):
    # TODO(bchetioui): Process transforms.
    if transforms_attr is not None:
      swizzle = swizzle_from_transforms_attr(transforms_attr)
      transforms = memref_transforms_from_transforms_attr(transforms_attr)
      if swizzle != mgpu.SwizzlingMode.kNoSwizzle or transforms:
        raise NotImplementedError(
            "Transformed or swizzled strided loads are not supported"
        )

    fragmented_array = fa.FragmentedArray.load_strided(
        transformed_ref,
        is_signed=is_signed,
        vec_size=out_layout.vec_size,
    )
    return [_fragmented_array_to_ir(fragmented_array)]

  if not isinstance(out_layout, fa.TiledLayout):
    raise ValueError(f"{op} has an unsupported layout: {out_layout_attr}")

  optimized = op.optimized.value if op.optimized is not None else None
  if transformed_ref.type.memory_space is None:  # GMEM
    fragmented_array = fa.FragmentedArray.load_untiled(
        transformed_ref,
        layout=out_layout,
        is_signed=is_signed,
        optimized=bool(optimized),
    )
    return [_fragmented_array_to_ir(fragmented_array)]

  if transforms_attr is None:
    raise ValueError(f"Unsupported memory space: {orig_ref_ty.memory_space}")

  swizzle = swizzle_from_transforms_attr(transforms_attr)
  transforms = memref_transforms_from_transforms_attr(transforms_attr)
  has_transforms = swizzle != mgpu.SwizzlingMode.kNoSwizzle or transforms
  if has_transforms:
    [tiling_transform] = transforms
    assert isinstance(tiling_transform, lc.TileTransform)

    def load_tiled(optimized: bool) -> fa.FragmentedArray:
      return fa.FragmentedArray.load_tiled(
          transformed_ref,
          swizzle,
          is_signed=is_signed,
          layout=out_layout,
          optimized=optimized,
          tiling_rank=len(tiling_transform.tiling)
      )

    fragmented_array = _retry_on_failure(load_tiled, optimized)
  else:

    def load_untiled(optimized: bool) -> fa.FragmentedArray:
      return fa.FragmentedArray.load_untiled(
          transformed_ref,
          layout=out_layout,
          is_signed=is_signed,
          optimized=optimized,
      )

    fragmented_array = _retry_on_failure(load_untiled, optimized)

  return [_fragmented_array_to_ir(fragmented_array)]

