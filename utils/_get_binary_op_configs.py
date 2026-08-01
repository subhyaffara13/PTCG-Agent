
def _get_binary_op_configs(
    dtype_configs: list[DTypeConfig],
) -> list[BackendPatternConfig]:
    binary_op_configs: list[BackendPatternConfig] = []
    num_tensor_args_to_observation_type_mapping = {
        # TODO: this is not used right now since we have extra check in prepare
        # will need to change this to NO_OBSERVER later after we implemented
        # Tensor dtype inference properly
        0: ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT,
        1: ObservationType.OUTPUT_SHARE_OBSERVER_WITH_INPUT,
        2: ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT,
    }
    for op_with_quantized_bop_scalar_variant in [
        operator.add,
        torch.add,
        operator.mul,
        torch.mul,
    ]:
        bop_patterns = [
            (op_with_quantized_bop_scalar_variant, nn.ReLU),
            (op_with_quantized_bop_scalar_variant, F.relu),
            (op_with_quantized_bop_scalar_variant, torch.relu),
            op_with_quantized_bop_scalar_variant,
        ]
        binary_op_configs.extend(
            BackendPatternConfig(bop_pattern)
            .set_dtype_configs(dtype_configs)  # noqa: E131
            ._set_num_tensor_args_to_observation_type(
                num_tensor_args_to_observation_type_mapping
            )
            for bop_pattern in bop_patterns
        )
    # matmul
    binary_op_configs.append(
        BackendPatternConfig(torch.matmul).set_dtype_configs(dtype_configs)  # noqa: E131
    )
    return binary_op_configs

