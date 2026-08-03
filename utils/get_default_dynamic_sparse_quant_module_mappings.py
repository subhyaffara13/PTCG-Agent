from typing import Any, Callable

def get_default_dynamic_sparse_quant_module_mappings() -> dict[Callable, Any]:
    """Get module mapping for post training dynamic sparse quantization"""
    return DEFAULT_DYNAMIC_SPARSE_QUANT_MODULE_MAPPINGS

