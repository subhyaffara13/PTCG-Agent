
def get_wrapper_codegen_for_device(
    device: str, cpp_wrapper: bool = False, fx_wrapper: bool = False
) -> WrapperConstructor | None:
    if device in device_codegens:
        wrapper_codegen_obj: DeviceCodegen = device_codegens[device]
        if fx_wrapper:
            return wrapper_codegen_obj.fx_wrapper_codegen
        elif cpp_wrapper:
            return wrapper_codegen_obj.cpp_wrapper_codegen
        else:
            return wrapper_codegen_obj.wrapper_codegen
    return None

