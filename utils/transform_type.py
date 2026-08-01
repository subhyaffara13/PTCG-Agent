
def transform_type(
    ts: Sequence[Transform], ty: core.AbstractValue
) -> core.AbstractValue:
  for t in ts:
    ty = t.transform_type(ty)
  return ty


def transform_type(
    ref_ty: ir.MemRefType,
    transforms: tuple[lc.MemRefTransform, ...] | ir.ArrayAttr,
) -> ir.MemRefType:
  if isinstance(transforms, ir.ArrayAttr):
    transforms = memref_transforms_from_transforms_attr(transforms)
  if not (utils.is_smem_ref(ref_ty) or utils.is_cluster_smem_ref(ref_ty)):
    raise ValueError(f"Only workgroup memory is supported but got {ref_ty}.")
  if utils.is_cluster_smem_ref(ref_ty):
    i32 = ir.IntegerType.get_signless(32)
    ref_ty = ir.MemRefType.get(
        ref_ty.shape,
        ref_ty.element_type,
        ref_ty.layout,
        memory_space=ir.IntegerAttr.get(i32, 7),
    )

  if not transforms:
    return ref_ty

  # TODO(bchetioui): this should be trivial to relax if ever necessary.
  if len(transforms) > 1 or not isinstance(transforms[0], lc.TileTransform):
    raise NotImplementedError(f"Unsupported transforms: {transforms}")
  tile_transform: lc.TileTransform = transforms[0]

  strides, offset = ref_ty.get_strides_and_offset()
  tiled_shape = tile_transform.transform_shape(ref_ty.shape)
  tiled_strides = tile_strides(tuple(strides), tile_transform.tiling)

  if offset == ir.ShapedType.get_dynamic_stride_or_offset():
    tiled_offset = offset
  else:
    delinearized_offset = [0] * len(strides)
    for i, stride in sorted(enumerate(strides), key=lambda es: es[1], reverse=True):
      delinearized_offset[i] = offset // stride
      offset %= stride
    tiled_delinearized_offset = tile_offset(
        tuple(delinearized_offset), tile_transform.tiling
    )
    tiled_offset = sum(o * s for o, s in zip(tiled_delinearized_offset, tiled_strides, strict=True))

  if isinstance(ref_ty.layout, ir.StridedLayoutAttr):
    layout = ir.StridedLayoutAttr.get(tiled_offset, tiled_strides)
  else:
    layout = None

  return ir.MemRefType.get(
      tiled_shape,
      ref_ty.element_type,
      memory_space=ref_ty.memory_space,
      layout=layout
  )

