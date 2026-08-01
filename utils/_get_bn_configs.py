
def _get_bn_configs() -> list[BackendPatternConfig]:
    """
    Return all configs related to batchnorm.
    """
    observation_type = ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
    dtype_configs = [
        qnnpack_default_op_qint8_symmetric_dtype_config,
        executorch_default_op_quint8_dtype_config,
    ]
    bn_configs = []
    bn_configs.append(
        BackendPatternConfig(nn.BatchNorm2d)
        .set_observation_type(observation_type)  # noqa: E131
        .set_dtype_configs(dtype_configs)
    )
    return bn_configs


def _get_bn_configs(dtype_configs: list[DTypeConfig]) -> list[BackendPatternConfig]:
    """Get configs related to batchnorm."""
    bn_configs = []
    bn_to_fused_bn = {
        torch.nn.BatchNorm2d: nni.BNReLU2d,
        torch.nn.BatchNorm3d: nni.BNReLU3d,
    }
    for bn in bn_to_fused_bn:
        fused_bn = bn_to_fused_bn[bn]
        # bn module + relu module fusion config
        bn_configs.append(
            BackendPatternConfig((bn, nn.ReLU))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(_sequential_wrapper2(fused_bn))
            .set_fused_module(fused_bn)
        )
        # bn module + F.relu fusion config
        bn_configs.append(
            BackendPatternConfig((bn, F.relu))
            .set_dtype_configs(dtype_configs)  # noqa: E131
            .set_fuser_method(_sequential_wrapper2(fused_bn))
            .set_fused_module(fused_bn)
        )
        bn_configs.append(
            BackendPatternConfig(bn)
            .set_observation_type(
                ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
            )  # noqa: E131
            .set_dtype_configs(dtype_configs)
        )

    # fused bn configs
    for fused_bn in bn_to_fused_bn.values():
        bn_configs.append(
            BackendPatternConfig(fused_bn)
            .set_observation_type(
                ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
            )  # noqa: E131
            .set_dtype_configs(dtype_configs)
        )
    return bn_configs

