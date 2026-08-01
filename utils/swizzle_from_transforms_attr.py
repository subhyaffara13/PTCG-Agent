
def swizzle_from_transforms_attr(attr: ir.ArrayAttr) -> mgpu.SwizzlingMode:
  swizzle = None
  for transform in attr:
    if isinstance(transform, mgpu.SwizzleTransformAttr):
      if swizzle is not None:
        raise ValueError("Found multiple SwizzleTransformAttr")
      swizzle = mgpu.SwizzlingMode(mgpu.SwizzleTransformAttr(transform).swizzle)
  return swizzle or mgpu.SwizzlingMode.kNoSwizzle

