
def _get_device_map(
    model: "PreTrainedModel",
    device_map: dict | str | None,
    max_memory: dict | None,
    hf_quantizer: "HfQuantizer | None",
) -> dict:
    """Compute the final `device_map` to use if we passed a value in ['auto', 'balanced', 'balanced_low_0', 'sequential'].
    Otherwise, we check for any device inconsistencies in the device_map.
    """
    if isinstance(device_map, str):
        no_split_modules = model._no_split_modules

        if device_map != "sequential":
            inferred_max_memory = get_balanced_memory(
                model,
                max_memory=max_memory,
                no_split_module_classes=no_split_modules,
                hf_quantizer=hf_quantizer,
                low_zero=(device_map == "balanced_low_0"),
            )
        else:
            inferred_max_memory = get_max_memory(max_memory)

        if hf_quantizer is not None:
            inferred_max_memory = hf_quantizer.adjust_max_memory(inferred_max_memory)

        device_map = infer_auto_device_map(
            model,
            max_memory=inferred_max_memory,
            no_split_module_classes=no_split_modules,
            hf_quantizer=hf_quantizer,
        )

        if hf_quantizer is not None:
            hf_quantizer.validate_environment(device_map=device_map)

    return device_map

