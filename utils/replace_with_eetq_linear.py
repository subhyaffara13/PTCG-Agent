
def replace_with_eetq_linear(model, modules_to_not_convert: list[str] | None = None, pre_quantized=False):
    """
    A helper function to replace all `torch.nn.Linear` modules by `EetqLinear` modules.

    Parameters:
        model (`torch.nn.Module`):
            Input model or `torch.nn.Module` as the function is run recursively.
        modules_to_not_convert (`list[`str`]`, *optional*, defaults to `None`):
            Names of the modules to not convert in `EetqLinear`. In practice we keep the `lm_head` in full precision
            for numerical stability reasons.
    """
    from .hub_kernels import get_kernel

    global eetq_kernels_hub
    eetq_kernels_hub = get_kernel("kernels-community/quantization-eetq")

    has_been_replaced = False
    # we need this to correctly materialize the weights during quantization
    module_kwargs = {} if pre_quantized else {"dtype": None}
    for module_name, module in model.named_modules():
        if not should_convert_module(module_name, modules_to_not_convert):
            continue
        with torch.device("meta"):
            if isinstance(module, nn.Linear):
                new_module = EetqLinear(
                    module.in_features, module.out_features, bias=module.bias is not None, **module_kwargs
                )
                model.set_submodule(module_name, new_module)
                has_been_replaced = True

    if not has_been_replaced:
        logger.warning(
            "You are loading your model using eetq but no linear modules were found in your model."
            " Please double check your model architecture, or submit an issue on github if you think this is"
            " a bug."
        )

    return model

