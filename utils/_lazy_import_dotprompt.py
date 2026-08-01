
def _lazy_import_dotprompt(name: str) -> Any:
    """Handler for dotprompt integration globals"""
    return _generic_lazy_import(name, _DOTPROMPT_IMPORT_MAP, "Dotprompt")

