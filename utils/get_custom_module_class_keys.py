
def get_custom_module_class_keys(
    custom_module_mapping: dict[QuantType, dict[type, type]],
) -> list[Any]:
    r"""Get all the unique custom module keys in the custom config dict
    e.g.
    Input:
    {
        QuantType.STATIC: {
            CustomModule1: ObservedCustomModule
        },
        QuantType.DYNAMIC: {
            CustomModule2: DynamicObservedCustomModule
        },
        QuantType.WEIGHT_ONLY: {
            CustomModule3: WeightOnlyObservedCustomModule
        },
    }

    Output:
    # extract the keys across all inner STATIC, DYNAMIC, and WEIGHT_ONLY dicts
    [CustomModule1, CustomModule2, CustomModule3]
    """
    # using set to dedup
    float_custom_module_classes: set[Any] = set()
    for quant_mode in [QuantType.STATIC, QuantType.DYNAMIC, QuantType.WEIGHT_ONLY]:
        quant_mode_custom_module_config = custom_module_mapping.get(quant_mode, {})
        quant_mode_custom_module_classes = set(quant_mode_custom_module_config.keys())
        float_custom_module_classes |= quant_mode_custom_module_classes
    return list(float_custom_module_classes)

