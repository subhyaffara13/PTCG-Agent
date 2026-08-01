
def get_pattern_to_input_type_to_index(
    backend_config: BackendConfig,
) -> dict[Pattern, dict[str, int]]:
    pattern_to_input_type_to_index: dict[Pattern, dict[str, int]] = {}
    for pattern, config in backend_config._pattern_complex_format_to_config.items():
        pattern_to_input_type_to_index[pattern] = config._input_type_to_index
    return pattern_to_input_type_to_index

