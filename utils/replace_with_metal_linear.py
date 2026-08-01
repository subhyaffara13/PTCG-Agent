
def replace_with_metal_linear(
    model,
    modules_to_not_convert: list[str] | None = None,
    quantization_config=None,
    pre_quantized: bool = False,
):
    """
    Replace every eligible ``nn.Linear`` with ``MetalLinear``.

    Args:
        model: the ``PreTrainedModel`` (on the meta device at this point).
        modules_to_not_convert: module names to leave untouched.
        quantization_config: the ``MetalConfig`` instance.
        pre_quantized: ``True`` when loading from a quantized checkpoint.
    """
    if quantization_config.dequantize:
        return model

    bits = quantization_config.bits
    group_size = quantization_config.group_size

    has_been_replaced = False

    for module_name, module in model.named_modules():
        if not should_convert_module(module_name, modules_to_not_convert):
            continue

        if isinstance(module, nn.Linear):
            module_kwargs = {} if pre_quantized else {"dtype": None}
            new_module = MetalLinear(
                in_features=module.in_features,
                out_features=module.out_features,
                bias=module.bias is not None,
                bits=bits,
                group_size=group_size,
                **module_kwargs,
            )

            model.set_submodule(module_name, new_module)
            has_been_replaced = True

    if not has_been_replaced:
        logger.warning(
            "You are loading a model with Metal quantization but no nn.Linear modules were found. "
            "Please double check your model architecture."
        )

    return model

