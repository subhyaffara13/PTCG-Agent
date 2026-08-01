
def _lazy_import_utils(name: str) -> Any:
    """Handler for utils module attributes (ModelResponse, token_counter, etc.)"""
    return _generic_lazy_import(name, _UTILS_IMPORT_MAP, "Utils")

