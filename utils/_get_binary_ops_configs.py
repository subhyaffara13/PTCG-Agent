
def _get_binary_ops_configs() -> list[BackendPatternConfig]:
    """
    Return all configs related to binary ops.
    """
    dtype_configs = [
        qnnpack_default_op_qint8_symmetric_dtype_config,
        executorch_weighted_op_int8_dtype_config,
    ]
    num_tensor_args_to_observation_type_mapping = {
        # TODO: this is not used right now since we have extra check in prepare
        # will need to change this to NO_OBSERVER later after we implemented
        # Tensor dtype inference properly
        0: ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT,
        1: ObservationType.OUTPUT_SHARE_OBSERVER_WITH_INPUT,
        2: ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT,
    }
    binary_op_configs: list[BackendPatternConfig] = []
    for op in [
        operator.add,
        torch.add,
        operator.sub,
        torch.sub,
        operator.mul,
        torch.mul,
    ]:
        bop_patterns = [
            (op, torch.nn.ReLU),
            (op, torch.nn.functional.relu),
            (op, torch.relu),
            op,
        ]
        binary_op_configs.extend(
            BackendPatternConfig(bop_pattern)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            ._set_num_tensor_args_to_observation_type(
                num_tensor_args_to_observation_type_mapping
            )
            for bop_pattern in bop_patterns
        )
    return binary_op_configs

