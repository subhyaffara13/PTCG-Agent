
def get_default_static_quant_reference_module_mappings() -> dict[Callable, Any]:
    """Get reference module mapping for post training static quantization"""
    return copy.deepcopy(DEFAULT_REFERENCE_STATIC_QUANT_MODULE_MAPPINGS)

