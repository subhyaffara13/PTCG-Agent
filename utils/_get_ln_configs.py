
def _get_ln_configs(dtype_configs: list[DTypeConfig]) -> list[BackendPatternConfig]:
    ln_configs = []
    ln_configs.append(
        BackendPatternConfig(torch.nn.LayerNorm)
        .set_observation_type(ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT)  # noqa: E131
        .set_dtype_configs(dtype_configs)
    )
    ln_configs.append(
        BackendPatternConfig(torch.nn.functional.layer_norm)
        .set_observation_type(ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT)  # noqa: E131
        .set_dtype_configs(dtype_configs)
        ._set_input_type_to_index({"weight": 2, "bias": 3})
    )
    return ln_configs

