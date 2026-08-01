
def memref_transforms_from_transforms_attr(
    attr: ir.ArrayAttr,
) -> tuple[lc.MemRefTransform, ...]:
  gmem_transforms: list[lc.MemRefTransform] = []
  for transform in attr:
    if isinstance(transform, mgpu.TileTransformAttr):
      tile_transform = lc.TileTransform(tuple(transform.tiling))
      gmem_transforms.append(tile_transform)
    elif not isinstance(transform, mgpu.SwizzleTransformAttr):
      raise NotImplementedError(f"Unsupported transform: {transform}")
  return tuple(gmem_transforms)

