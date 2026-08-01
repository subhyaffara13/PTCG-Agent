
def aot_stage2_compile(
    aot_state: AOTState,
    aot_graph_capture: AOTGraphCapture,
    # pyrefly: ignore [implicit-any]
    partition_fn: Callable,
    # pyrefly: ignore [implicit-any]
    fw_compiler: Callable,
    # pyrefly: ignore [implicit-any]
    bw_compiler: Callable | None = None,
    # pyrefly: ignore [implicit-any]
    inference_compiler: Callable | None = None,
) -> DispatchReturn:
    if bw_compiler is None:
        bw_compiler = fw_compiler
    if inference_compiler is None:
        inference_compiler = fw_compiler
    # Update the AOTState with the provided compilers
    aot_state.aot_config.partition_fn = partition_fn
    aot_state.aot_config.fw_compiler = fw_compiler
    aot_state.aot_config.bw_compiler = bw_compiler
    aot_state.aot_config.inference_compiler = inference_compiler

    if aot_state.needs_autograd and not aot_state.aot_config.pre_dispatch:
        return aot_stage2_autograd(aot_state, aot_graph_capture)
    else:
        return aot_stage2_inference(aot_state, aot_graph_capture)

