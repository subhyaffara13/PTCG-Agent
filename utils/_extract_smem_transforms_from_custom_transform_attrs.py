
def _extract_smem_transforms_from_custom_transform_attrs(
    ref_type: ir.MemRefType,
    transform_attrs: ir.ArrayAttr,
) -> cs.SMEMTransforms:
  transforms = [layouts_lib.from_transform_attr(x) for x in transform_attrs]
  match transforms:
    case []:
      tile_transform = None
      swizzle = None
    case [lc.TileTransform() as t]:
      tile_transform = t
      swizzle = None
    case [lc.TileTransform() as t, mgpu.SwizzlingMode() as s]:
      tile_transform = t
      swizzle = s
    case _:
      raise NotImplementedError(f"Unsupported transforms {transforms}")

  if swizzle is not None:
    computed_swizzle = _compute_swizzle(ref_type, tile_transform)
    if computed_swizzle != swizzle:
      raise NotImplementedError(
          f"Cannot honor caller-provided swizzle {swizzle} that is different "
          f"from the computed swizle {computed_swizzle} for type {ref_type}."
      )

  return cs.SMEMTransforms(tile_transform)

