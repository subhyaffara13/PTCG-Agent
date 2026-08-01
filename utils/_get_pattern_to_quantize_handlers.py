
def _get_pattern_to_quantize_handlers(
    backend_config: BackendConfig,
) -> dict[Pattern, QuantizerCls]:
    """
    Note: Quantize handler is just a holder for some check methods like
    (should_insert_observer_for_output), maybe this can be a enum as well,
    we can refactor this after we convert the path for fbgemm/qnnpack fully to the
    new path, this is not exposed to backend developers
    """
    pattern_to_quantize_handlers = {}
    for pattern, config in backend_config._pattern_complex_format_to_config.items():
        observation_type = config.observation_type
        dtype_configs = config.dtype_configs
        num_tensor_args_to_observation_type = (
            config._num_tensor_args_to_observation_type
        )
        pattern_to_quantize_handlers[pattern] = _get_quantize_handler_cls(
            observation_type, dtype_configs, num_tensor_args_to_observation_type
        )
    return pattern_to_quantize_handlers

