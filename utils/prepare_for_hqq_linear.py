
def prepare_for_hqq_linear(model, quantization_config=None, modules_to_not_convert=None, has_been_replaced=False):
    """
    Prepares nn.Linear layers for HQQ quantization.
    Since each layer type can have separate quantization parameters, we need to do the following:
    1- tag each module with its name via autoname_modules()
    2- Extract linear_tags (e.g. ['self_attn.q_proj', ...])
    3- Map quantization parameters as a dictionary linear_tag -> quant_params as HQQLinear expects it, this is referred to as patch_params
    """

    modules_to_not_convert = [] if modules_to_not_convert is None else modules_to_not_convert

    # Add name to module
    autoname_modules(model)

    # Get linear tags. This allows us to use different quant params to different layer types
    linear_tags = get_linear_tags(model)

    # Convert quantization_config to layer-wise config
    skip_modules = quantization_config.skip_modules
    quant_config = quantization_config.quant_config
    linear_tags = list(set(linear_tags) - set(skip_modules) - set(modules_to_not_convert))

    if any(key in linear_tags for key in quant_config):
        # If the user doesn't specify a key from get_linear_tags, the layer is not quantized via (key, None)
        patch_params = dict.fromkeys(linear_tags)
        patch_params.update(quant_config)
    else:
        # Same quant_config for all layers
        patch_params = dict.fromkeys(linear_tags, quant_config)

    model, has_been_replaced = _prepare_for_hqq_linear(
        model, patch_params=patch_params, has_been_replaced=has_been_replaced
    )

    # We store quantization config as linear_tag -> hqq quant config
    model.config.quantization_config = {
        "quant_config": quant_config,
        "quant_method": quantization_config.quant_method,
        "skip_modules": skip_modules,
    }

    if not has_been_replaced:
        logger.warning("No linear modules were found in your model for quantization.")

    return model

