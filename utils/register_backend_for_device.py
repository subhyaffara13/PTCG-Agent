
def register_backend_for_device(
    device: str,
    device_scheduling: SchedulingConstructor,
    device_wrapper_codegen: WrapperConstructor,
    device_cpp_wrapper_codegen: WrapperConstructor | None = None,
    device_fx_wrapper_codegen: WrapperConstructor | None = None,
    device_custom_pass: CustomGraphModulePass | None = None,
    device_custom_config: ConfigModule | None = None,
) -> None:
    device_codegens[device] = DeviceCodegen(
        device_scheduling,
        device_wrapper_codegen,
        device_cpp_wrapper_codegen,
        device_fx_wrapper_codegen,
    )
    custom_backend_passes[device] = device_custom_pass
    if device_custom_config:
        assert (
            isinstance(device_custom_config, ConfigModule)
            and device_custom_config is not config
        ), (
            f"{device_custom_config=} cannot be the same as the default inductor config {config=}"
        )
    custom_backend_codegen_configs[device] = device_custom_config

