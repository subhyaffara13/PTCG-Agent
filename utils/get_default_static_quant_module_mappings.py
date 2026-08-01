
def get_default_static_quant_module_mappings() -> dict[Callable, Any]:
    """Get module mapping for post training static quantization"""
    return copy.deepcopy(DEFAULT_STATIC_QUANT_MODULE_MAPPINGS)

