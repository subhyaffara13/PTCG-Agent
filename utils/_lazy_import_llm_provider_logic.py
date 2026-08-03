from typing import Any

def _lazy_import_llm_provider_logic(name: str) -> Any:
    """Handler for LLM provider logic functions (get_llm_provider, etc.)"""
    return _generic_lazy_import(
        name, _LLM_PROVIDER_LOGIC_IMPORT_MAP, "LLM provider logic"
    )

