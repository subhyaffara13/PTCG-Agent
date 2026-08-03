import copy
from typing import Any, Callable

def get_default_static_sparse_quant_module_mappings() -> dict[Callable, Any]:
    """Get module mapping for post training static sparse quantization"""
    return copy.deepcopy(DEFAULT_STATIC_SPARSE_QUANT_MODULE_MAPPINGS)

