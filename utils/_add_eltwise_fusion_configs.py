
def _add_eltwise_fusion_configs(
    configs,
    root_module,
    root_op,
    post_module,
    post_op,
    dtype_configs,
    fuser_method,
    fused_module,
    observation_type,
    ref_quant_module,
):
    # 1 base module + op module fusion config
    configs.append(
        BackendPatternConfig((root_module, post_module))
        .set_dtype_configs(dtype_configs)  # noqa: E131
        .set_fuser_method(fuser_method)
        .set_fused_module(fused_module)
    )
    # base module + functional post op
    configs.append(
        BackendPatternConfig((root_module, post_op))
        .set_dtype_configs(dtype_configs)  # noqa: E131
        .set_fuser_method(fuser_method)
        .set_fused_module(fused_module)
    )

    # 2 fused module configs
    configs.append(
        BackendPatternConfig(fused_module)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        .set_root_module(root_module)
        .set_reference_quantized_module(ref_quant_module)
    )

    # 3 functional base op + post op configs
    configs.append(
        BackendPatternConfig((root_op, post_module))
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
    )
    configs.append(
        BackendPatternConfig((root_op, post_op))
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
    )

