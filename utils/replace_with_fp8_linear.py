
def replace_with_fp8_linear(
    model, modules_to_not_convert: list[str] | None = None, quantization_config=None, pre_quantized=False
):
    """
    A helper function to replace all `torch.nn.Linear` modules by `FP8Linear` modules.

    Parameters:
        model (`torch.nn.Module`):
            Input model or `torch.nn.Module` as the function is run recursively.
        modules_to_not_convert (`list[`str`]`, *optional*, defaults to `None`):
            Names of the modules to not convert. In practice we keep the `lm_head` in full precision for numerical stability reasons.
        quantization_config (`FineGrainedFP8Config`):
            The quantization config object that contains the quantization parameters.
        pre_quantized (`book`, defaults to `False`):
            Whether the model is pre-quantized or not
    """

    if quantization_config.dequantize:
        return model

    has_been_replaced = False
    for module_name, module in model.named_modules():
        if not should_convert_module(module_name, modules_to_not_convert):
            continue

        new_module = None
        with torch.device("meta"):
            if module_name.endswith(".experts"):
                has_gate = getattr(module, "has_gate", True)
                has_bias = getattr(module, "has_bias", False)
                config = getattr(module, "config", model.config.get_text_config())
                new_class = use_experts_implementation(
                    experts_class=FP8Experts,
                    experts_interface=ALL_FP8_EXPERTS_FUNCTIONS,
                    has_bias=has_bias,
                    has_gate=has_gate,
                )
                new_module = new_class(
                    config=config,
                    block_size=quantization_config.weight_block_size,
                    activation_scheme=quantization_config.activation_scheme,
                    scale_fmt=quantization_config.scale_fmt,
                    has_bias=has_bias,
                    has_gate=has_gate,
                )
            elif type(module) is nn.Linear:
                # Vanilla `nn.Linear` → standard FP8Linear swap.
                new_module = FP8Linear(
                    in_features=module.in_features,
                    out_features=module.out_features,
                    block_size=quantization_config.weight_block_size,
                    activation_scheme=quantization_config.activation_scheme,
                    scale_fmt=quantization_config.scale_fmt,
                    has_bias=module.bias is not None,
                )
            elif isinstance(module, nn.Linear) and "GroupedLinear" in type(module).__name__:
                # Block-diagonal grouped linear (e.g. DSv4's `DeepseekV4GroupedLinear`):
                # one underlying weight conceptually split into `n_groups` independent
                # sub-matmuls fed by disjoint input slices. Vanilla `FP8Linear` would
                # collapse those groups into one giant linear and yield the wrong
                # output dim, so swap to `FP8GroupedLinear` which keeps the per-group
                # bmm contract and runs each block as its own FP8 matmul.
                new_module = FP8GroupedLinear(
                    in_features_per_group=module.in_features,
                    out_features=module.out_features,
                    n_groups=module.n_groups,
                    block_size=quantization_config.weight_block_size,
                    activation_scheme=quantization_config.activation_scheme,
                    scale_fmt=quantization_config.scale_fmt,
                    has_bias=module.bias is not None,
                )
            if new_module is not None:
                model.set_submodule(module_name, new_module)
                has_been_replaced = True

    if not has_been_replaced:
        logger.warning(
            "You are loading your model using fp8 but no linear modules were found in your model."
            " Please double check your model architecture."
        )
    return model

