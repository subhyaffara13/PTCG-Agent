
def _lazy_import_token_counter(name: str) -> Any:
    """Handler for token counter utilities"""
    return _generic_lazy_import(name, _TOKEN_COUNTER_IMPORT_MAP, "Token counter")

