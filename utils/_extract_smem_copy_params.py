
def _extract_smem_copy_params(aval, transforms):
  if not transforms:
    return {}
  # Split off swizzling, if present
  match transforms:
    case [gpu_core.UnswizzleRef(swizzle), *transforms]:
      pass
    case _:
      swizzle = None
  reversed_transforms = pallas_core.undo_transforms(aval, transforms)
  gpu_transforms = tuple(
      gpu_core.to_gpu_transform(t) for t in reversed_transforms
  )
  return dict(
      gmem_transform=gpu_transforms,
      swizzle=swizzle,
  )

