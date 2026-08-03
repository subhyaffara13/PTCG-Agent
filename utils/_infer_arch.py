from typing import Any

def _infer_arch() -> tuple[int, int]:
  device: Any = jax.sharding.get_abstract_mesh().abstract_device
  if device is None:
    device = jex_backend.get_default_device()
  if not hasattr(device, "compute_capability"):
    return (9, 0)  # TODO(apaszke): Remove this once we figure out the export story.
  arch_name = device.compute_capability
  # Handle ROCm devices that return architecture strings like "gfxXXX".
  if arch_name.startswith("gfx"):
    raise ValueError(
        f"Mosaic GPU does not yet support AMD ROCm devices. "
        f"Got compute_capability: {arch_name}"
    )
  return tuple(map(int, arch_name.split(".")))  # pyrefly: ignore[bad-return]

