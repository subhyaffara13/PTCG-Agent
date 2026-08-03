from typing import Any

def _normalize_specs(specs: Any) -> tuple[pallas_core.BlockSpec, ...]:
  if not isinstance(specs, (list, tuple)):
    specs = (specs,)
  if isinstance(specs, list):
    specs = tuple(specs)
  return specs

