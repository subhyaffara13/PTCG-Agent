
def get_pattern_to_dtype_configs(
    backend_config: BackendConfig,
) -> dict[Pattern, list[DTypeConfig]]:
    pattern_to_dtype_configs: dict[Pattern, list[DTypeConfig]] = {}
    for pattern, config in backend_config._pattern_complex_format_to_config.items():
        pattern_to_dtype_configs[pattern] = config.dtype_configs
    return pattern_to_dtype_configs

