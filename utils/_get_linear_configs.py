
def _get_linear_configs() -> list[BackendPatternConfig]:
    """
    Return all configs related to linear modules and ops.
    """
    observation_type = ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
    dtype_configs = [
        qnnpack_weighted_op_qint8_symmetric_dtype_config,
        executorch_weighted_op_int8_dtype_config,
        executorch_default_dynamic_quint8_dtype_config,
        executorch_default_dynamic_qint8_dtype_config,
        executorch_default_dynamic_float16_dtype_config,
    ]
    linear_configs: list[BackendPatternConfig] = []
    # linear module
    linear_configs.append(
        BackendPatternConfig(torch.nn.Linear)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        .set_root_module(torch.nn.Linear)
        .set_reference_quantized_module(nnqr.Linear)
        .set_qat_module(nnqat.Linear)
    )
    # linear qat module
    linear_configs.append(
        BackendPatternConfig(nnqat.Linear)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        .set_root_module(torch.nn.Linear)
        .set_reference_quantized_module(nnqr.Linear)
    )
    # functional linear
    linear_configs.append(
        BackendPatternConfig(torch.nn.functional.linear)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        ._set_input_type_to_index({"weight": 1, "bias": 2})
    )
    return linear_configs


def _get_linear_configs(dtype_configs: list[DTypeConfig]) -> list[BackendPatternConfig]:
    """
    Return all configs related to linear modules and ops.
    """
    observation_type = ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
    linear_configs: list[BackendPatternConfig] = []

    # (1) Single linear modules/functions
    # -------------------------------------
    # linear module
    linear_configs.append(
        BackendPatternConfig(torch.nn.Linear)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        .set_root_module(torch.nn.Linear)
        .set_reference_quantized_module(nnqr.Linear)
        .set_qat_module(nnqat.Linear)
    )
    # linear qat module
    linear_configs.append(
        BackendPatternConfig(nnqat.Linear)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        .set_root_module(torch.nn.Linear)
        .set_reference_quantized_module(nnqr.Linear)
    )
    # functional linear
    linear_configs.append(
        BackendPatternConfig(torch.nn.functional.linear)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        ._set_input_type_to_index({"weight": 1, "bias": 2})
    )

    # (2) Linear + relu
    # -------------------
    # 2.1 linear module + relu fusion config
    # linear relu, linear module + relu module
    linear_configs.append(
        BackendPatternConfig((torch.nn.Linear, torch.nn.ReLU))
        .set_dtype_configs(dtype_configs)  # noqa: E131
        .set_fuser_method(_sequential_wrapper2(nni.LinearReLU))
        .set_fused_module(nni.LinearReLU)
    )
    # linear relu, linear module + functional relu
    linear_configs.append(
        BackendPatternConfig((torch.nn.Linear, torch.nn.functional.relu))
        .set_dtype_configs(dtype_configs)  # noqa: E131
        .set_fuser_method(_sequential_wrapper2(nni.LinearReLU))
        .set_fused_module(nni.LinearReLU)
    )

    # 2.2 linear module + relu, fused module configs
    # linear relu, fused module
    linear_configs.append(
        BackendPatternConfig(nni.LinearReLU)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        .set_root_module(torch.nn.Linear)
        .set_reference_quantized_module(nnqr.Linear)
        .set_qat_module(nniqat.LinearReLU)
    )
    # linear relu, qat fused module
    linear_configs.append(
        BackendPatternConfig(nniqat.LinearReLU)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        .set_root_module(torch.nn.Linear)
        .set_reference_quantized_module(nnqr.Linear)
    )
    # 2.3 functional linear + relu configs
    # linear relu, functional linear + relu module
    linear_configs.append(
        BackendPatternConfig((F.linear, torch.nn.ReLU))
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
    )
    # linear relu, functional linear + functional relu
    linear_configs.append(
        BackendPatternConfig((F.linear, F.relu))
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
    )

    # (3) Linear + batchnorm
    # ------------------------
    # 3.1 linear bn fusion
    linear_configs.append(
        BackendPatternConfig((nn.Linear, nn.BatchNorm1d))
        .set_dtype_configs(dtype_configs)  # noqa: E131
        .set_fuser_method(fuse_linear_bn)
        .set_fused_module(nni.LinearBn1d)
    )

    # 3.2 linear bn fused
    # linear bn, fused module
    linear_configs.append(
        BackendPatternConfig(nni.LinearBn1d)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        .set_root_module(torch.nn.Linear)
        .set_reference_quantized_module(nnqr.Linear)
        .set_qat_module(nniqat.LinearBn1d)
    )
    # linear bn, qat fused module
    linear_configs.append(
        BackendPatternConfig(nniqat.LinearBn1d)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        .set_root_module(torch.nn.Linear)
        .set_reference_quantized_module(nnqr.Linear)
    )
    return linear_configs

