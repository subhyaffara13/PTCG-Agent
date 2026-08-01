
def get_custom_backend_config_for_device(device: str) -> ConfigModule | None:
    return custom_backend_codegen_configs.get(device)

