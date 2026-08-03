from typing import Any

def array_conversion(value: Any, xp: ModuleType, device: Device | None = None) -> Any:
    """Convert a value into the specified xp module array type."""
    raise Exception(
        f"No known conversion for ({type(value)}) to xp module ({xp}) registered. Report as issue on github."
    )

