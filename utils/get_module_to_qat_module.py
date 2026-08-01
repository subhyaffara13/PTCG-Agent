
def get_module_to_qat_module(
    backend_config: BackendConfig,
) -> dict[Pattern, type[torch.nn.Module]]:
    module_to_qat_module: dict[Pattern, type[torch.nn.Module]] = {}
    for pattern, config in backend_config._pattern_complex_format_to_config.items():
        if config.qat_module is not None:
            module_to_qat_module[pattern] = config.qat_module
    return module_to_qat_module

