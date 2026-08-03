from typing import Any

def _lazy_import_types(name: str) -> Any:
    """Handler for type classes (GuardrailItem, etc.)"""
    return _generic_lazy_import(name, _TYPES_IMPORT_MAP, "Types")

