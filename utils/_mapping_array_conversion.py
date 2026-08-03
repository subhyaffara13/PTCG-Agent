from typing import Any

def _mapping_array_conversion(
    value: Mapping[str, Any], xp: ModuleType, device: Device | None = None
) -> Mapping[str, Any]:
    """Convert a mapping of Arrays into a Dictionary of the specified xp module array type."""
    return type(value)(**{k: array_conversion(v, xp, device) for k, v in value.items()})

