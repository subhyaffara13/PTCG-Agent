
def replace_with_higgs_linear(model, modules_to_not_convert: list[str] | None = None, quantization_config=None):
    """
    Public method that replaces the Linear layers of the given model with HIGGS quantized layers.

    Args:
        model (`torch.nn.Module`):
            The model to convert, can be any `torch.nn.Module` instance.
        modules_to_not_convert (`list[str]`, *optional*, defaults to `None`):
            A list of nn.Linear weights to not convert. If a parameter path is in the list (e.g. `lm_head.weight`), the corresponding module will not be
            converted.
        quantization_config (`HiggsConfig`):
            The quantization config object that contains the quantization parameters.
    """

    has_been_replaced = False
    # we need this to correctly materialize the weights during quantization
    for module_name, module in model.named_modules():
        if not should_convert_module(module_name, modules_to_not_convert):
            continue
        with torch.device("meta"):
            if isinstance(module, nn.Linear):
                new_module = HiggsLinear(
                    module.in_features,
                    module.out_features,
                    bias=module.bias is not None,
                    num_bits=quantization_config.bits,
                    hadamard_size=quantization_config.hadamard_size,
                    group_size=quantization_config.group_size,
                )
                new_module.source_cls = type(module)
                new_module.requires_grad_(False)
                model.set_submodule(module_name, new_module)
                has_been_replaced = True

    if not has_been_replaced:
        logger.warning(
            "You are loading your model using eetq but no linear modules were found in your model."
            " Please double check your model architecture, or submit an issue on github if you think this is"
            " a bug."
        )
    return model

