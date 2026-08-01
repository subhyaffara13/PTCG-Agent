
def get_qat_module_classes(backend_config: BackendConfig) -> tuple[type, ...]:
    qat_module_classes = [
        config.qat_module
        for config in backend_config.configs
        if config.qat_module is not None
    ]
    return tuple(set(qat_module_classes))

