
def from_transform_attr(
    transform: ir.Attribute,
) -> launch_context.MemRefTransform | mgpu.SwizzlingMode:
  if isinstance(transform, mgpu.TileTransformAttr):
    return launch_context.TileTransform(
        tuple(mgpu.TileTransformAttr(transform).tiling)
    )
  elif isinstance(transform, mgpu.SwizzleTransformAttr):
    return mgpu.SwizzlingMode(mgpu.SwizzleTransformAttr(transform).swizzle)
  else:
    raise NotImplementedError(f"Unsupported transform {transform}")

