
def create_fx_config(
    compiler_config_extra: CompilerConfigExtra | None = None,
    compile_region_name: str | None = None,
) -> _CompileFxKwargs:
    if compiler_config_extra is None:
        cudagraphs = BoxedBool(torch._inductor.config.triton.cudagraphs)
        boxed_forward_device_index = None
    else:
        cudagraphs = compiler_config_extra.cudagraphs
        boxed_forward_device_index = compiler_config_extra.forward_device
    return {
        "cudagraphs": cudagraphs,
        "boxed_forward_device_index": boxed_forward_device_index,
        "compile_region_name": compile_region_name,  # pyrefly: ignore[bad-typed-dict-key]
    }

