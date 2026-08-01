
def _none_array_conversion(
    value: None, xp: ModuleType, device: Device | None = None
) -> None:
    """Passes through None values."""
    return value

