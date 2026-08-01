
def get_fused_module_classes(backend_config: BackendConfig) -> tuple[type, ...]:
    fused_module_classes = [
        config.fused_module
        for config in backend_config.configs
        if config.fused_module is not None
    ]
    return tuple(set(fused_module_classes))

