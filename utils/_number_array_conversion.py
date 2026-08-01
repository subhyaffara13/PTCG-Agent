
def _number_array_conversion(
    value: numbers.Number, xp: ModuleType, device: Device | None = None
) -> Array:
    """Convert a python number (int, float, complex) to an Array API framework array."""
    return xp.asarray(value, device=device)

