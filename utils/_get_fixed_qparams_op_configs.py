
def _get_fixed_qparams_op_configs(
    dtype_configs: list[DTypeConfig],
) -> list[BackendPatternConfig]:
    fixed_qparams_op_configs = []
    for fixed_qparam_op, constraints in _FIXED_QPARAMS_OP_TO_CONSTRAINTS.items():
        new_dtype_configs = _add_fixed_qparams_to_dtype_configs(
            dtype_configs, constraints
        )
        fixed_qparams_op_configs.append(
            BackendPatternConfig(fixed_qparam_op)
            .set_observation_type(
                ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
            )  # noqa: E131
            .set_dtype_configs(new_dtype_configs)
        )
    return fixed_qparams_op_configs

