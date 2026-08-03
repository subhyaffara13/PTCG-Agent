from typing import Callable

def get_fuser_method_mapping(
    backend_config: BackendConfig,
) -> dict[Pattern, nn.Sequential | Callable]:
    fuser_method_mapping: dict[Pattern, nn.Sequential | Callable] = {}
    for pattern, config in backend_config._pattern_complex_format_to_config.items():
        if config.fuser_method is not None:
            # Note: both the fuser method and the pattern are specified in forward order in the
            # BackendConfig, but the internal pattern matching code uses the reversed nested tuple
            # format, so we need to convert both to the internal format
            fuser_method = _get_fuser_method_in_reversed_nested_tuple_format(config)
            fuser_method_mapping[pattern] = fuser_method
    return fuser_method_mapping

