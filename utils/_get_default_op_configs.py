
def _get_default_op_configs(
    dtype_configs: list[DTypeConfig],
) -> list[BackendPatternConfig]:
    default_ops = [
        torch.nn.ELU,
        torch.nn.LeakyReLU,
        torch.nn.Hardswish,
        torch.nn.InstanceNorm1d,
        torch.nn.InstanceNorm2d,
        torch.nn.InstanceNorm3d,
        torch.nn.Dropout,
        torch.nn.PReLU,
        torch.nn.functional.elu,
        torch.nn.functional.hardswish,
        torch.nn.functional.leaky_relu,
        torch.nn.functional.dropout,
    ]
    configs = [
        BackendPatternConfig(op)
        .set_observation_type(ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        for op in default_ops
    ]

    configs.append(
        BackendPatternConfig(torch.nn.functional.group_norm)
        .set_observation_type(ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        ._set_input_type_to_index({"weight": 2, "bias": 3})
    )

    configs.append(
        BackendPatternConfig(torch.nn.functional.instance_norm)
        .set_observation_type(ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        ._set_input_type_to_index({"weight": 3, "bias": 4})
    )
    return configs

