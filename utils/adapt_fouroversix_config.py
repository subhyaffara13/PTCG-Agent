
def adapt_fouroversix_config(config: FourOverSixConfig):
    return ModelQuantizationConfig(
        activation_dtype=config.activation_dtype,
        activation_scale_rule=config.activation_scale_rule,
        dtype=config.dtype,
        gradient_dtype=config.gradient_dtype,
        gradient_scale_rule=config.gradient_scale_rule,
        keep_master_weights=config.keep_master_weights,
        matmul_backend=config.matmul_backend,
        output_dtype=config.output_dtype,
        quantize_backend=config.quantize_backend,
        scale_rule=config.scale_rule,
        weight_dtype=config.weight_dtype,
        weight_scale_2d=config.weight_scale_2d,
        weight_scale_rule=config.weight_scale_rule,
        modules_to_not_convert=config.modules_to_not_convert,
        module_config_overrides=config.module_config_overrides,
    )

