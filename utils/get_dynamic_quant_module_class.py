
def get_dynamic_quant_module_class(
    float_module_class: Callable,
    additional_dynamic_quant_mapping: dict[Callable, Any] | None = None,
) -> Any:
    r"""n Get the dynamically quantized module class corresponding to
    the floating point module class
    """
    if additional_dynamic_quant_mapping is None:
        additional_dynamic_quant_mapping = {}
    all_mappings = get_combined_dict(
        DEFAULT_DYNAMIC_QUANT_MODULE_MAPPINGS, additional_dynamic_quant_mapping
    )
    dynamic_quant_module_class = all_mappings.get(float_module_class, None)
    if dynamic_quant_module_class is None:
        raise AssertionError(
            f"Floating point module class {str(float_module_class)}"
            + " does not have a corresponding quantized module class"
        )
    return copy.deepcopy(dynamic_quant_module_class)

