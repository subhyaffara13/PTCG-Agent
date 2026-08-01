
def get_default_qat_module_mappings() -> dict[Callable, Any]:
    """Get default module mapping for quantization aware training"""
    return copy.deepcopy(DEFAULT_QAT_MODULE_MAPPINGS)

