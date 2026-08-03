from typing import Any

def _lazy_import_litellm_logging(name: str) -> Any:
    """Handler for litellm_logging module (Logging, modify_integration)"""
    return _generic_lazy_import(name, _LITELLM_LOGGING_IMPORT_MAP, "Litellm logging")

