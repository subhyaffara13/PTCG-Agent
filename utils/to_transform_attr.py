
def to_transform_attr(
    transform: state_types.Transform,
) -> ir.Attribute:
  match transform:
    case SwizzleTransform(swizzle):
      return mgpu.dialect.SwizzleTransformAttr.get(swizzle)
    case _:
      return to_gpu_transform(transform).to_attr()


def to_transform_attr(
    transform: launch_context.MemRefTransform | mgpu.SwizzlingMode,
) -> ir.Attribute:
  if isinstance(transform, launch_context.TileTransform):
    return mgpu.TileTransformAttr.get(transform.tiling)
  elif isinstance(transform, mgpu.SwizzlingMode):
    return mgpu.SwizzleTransformAttr.get(transform)
  else:
    raise NotImplementedError(f"Unsupported transform {transform}")

