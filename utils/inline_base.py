
def inline_base(name: str, index: int) -> str:
    """Synthetic name to use when storing inlined base classes in symbol tables."""
    return f"{name}@base{index + 1}"

