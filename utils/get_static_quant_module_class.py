
def get_static_quant_module_class(
    float_module_class: Callable,
    additional_static_quant_mapping: dict[Callable, Any] | None = None,
    is_reference: bool = False,
) -> Any:
    r"""n Get the statically quantized module class corresponding to
    the floating point module class
    """
    if additional_static_quant_mapping is None:
        additional_static_quant_mapping = {}
    all_mappings = get_combined_dict(
        DEFAULT_REFERENCE_STATIC_QUANT_MODULE_MAPPINGS
        if is_reference
        else DEFAULT_STATIC_QUANT_MODULE_MAPPINGS,
        additional_static_quant_mapping,
    )
    static_quant_module_class = all_mappings.get(float_module_class, None)
    if static_quant_module_class is None:
        raise AssertionError(
            f"Floating point module class {str(float_module_class)}"
            + " does not have a corresponding quantized module class"
        )
    return copy.deepcopy(static_quant_module_class)

