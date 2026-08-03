from typing import Any, Callable

def get_default_dynamic_quant_module_mappings() -> dict[Callable, Any]:
    """Get module mapping for post training dynamic quantization"""
    return DEFAULT_DYNAMIC_QUANT_MODULE_MAPPINGS

