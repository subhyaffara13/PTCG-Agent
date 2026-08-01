
def patch_inductor_backend(
    device: str,
    python_wrapper_codegen: PythonWrapperCodegen = None,
    custom_pass: CustomGraphModulePass = None,
    custom_backend_config: ConfigModule = None,
):
    """
    Patch the inductor backend for a specific device.
    """
    # Make sure the backend is already registered
    init_backend_registration()

    # Get the original registration parameters
    original_scheduling = get_scheduling_for_device(device)
    original_python_wrapper = get_wrapper_codegen_for_device(device, False)
    original_cpp_wrapper = get_wrapper_codegen_for_device(device, True)
    original_fx_wrapper = get_wrapper_codegen_for_device(device, fx_wrapper=True)
    original_custom_pass = get_custom_backend_pass_for_device(device)
    original_custom_backend_config = get_custom_backend_config_for_device(device)

    try:
        # Register modified backend for the device
        register_backend_for_device(
            device,
            original_scheduling,
            (
                python_wrapper_codegen
                if python_wrapper_codegen is not None
                else original_python_wrapper
            ),
            original_cpp_wrapper,
            original_fx_wrapper,
            custom_pass if custom_pass is not None else original_custom_pass,
            (
                custom_backend_config
                if custom_backend_config is not None
                else original_custom_backend_config
            ),
        )
        yield
    finally:
        # Restore the original backend
        register_backend_for_device(
            device,
            original_scheduling,
            original_python_wrapper,
            original_cpp_wrapper,
            original_fx_wrapper,
            original_custom_pass,
            original_custom_backend_config,
        )

