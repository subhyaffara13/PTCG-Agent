
def get_root_module_to_quantized_reference_module(
    backend_config: BackendConfig,
) -> dict[type[torch.nn.Module], type[torch.nn.Module]]:
    mapping: dict[type[torch.nn.Module], type[torch.nn.Module]] = {}
    for config in backend_config.configs:
        if (
            config.root_module is not None
            and config.reference_quantized_module is not None
        ):
            mapping[config.root_module] = config.reference_quantized_module
    return mapping

