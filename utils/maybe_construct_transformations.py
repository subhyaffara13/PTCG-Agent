from typing import Any

def maybe_construct_transformations(
  target: Any, transforms: Any | None
) -> Any:
  if transforms is not None:
    return transforms
  flat_transforms = {}
  flat_target = ocp.utils.to_flat_dict(target, sep='/', keep_empty_nodes=True)
  for k, v in flat_target.items():
    if v is None:
      flat_transforms[k] = ocp.Transform(use_fallback=True)
  return flat_transforms

