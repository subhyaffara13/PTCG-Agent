
def _lazy_import_types_utils(name: str) -> Any:
    """Handler for types from litellm.types.utils (BudgetConfig, ImageObject, etc.)"""
    return _generic_lazy_import(name, _TYPES_UTILS_IMPORT_MAP, "Types utils")

