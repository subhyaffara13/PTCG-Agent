from typing import Any, Callable

def _aot_stage2c_make_inference_function(
    aot_config: AOTConfig,
    fw_metadata: ViewAndMutationMeta,
    compiled_fw: Callable[..., Any],
    wrappers: list[CompilerWrapper],
    entry: GenericAOTAutogradResult[Any, Any] | None,
) -> DispatchReturn:
    if entry is not None:
        compiled_fw = SerializableCompiledFunction(compiled_fw, lambda: entry)

    disable_amp = torch._C._is_any_autocast_enabled()
    compiled_fn = RuntimeWrapper(
        indices_of_inps_to_detach=[],
        trace_joint=False,
        disable_amp=disable_amp,
    ).post_compile(
        compiled_fw,
        aot_config,
        runtime_metadata=fw_metadata,
    )

    compiled_fn = post_compile(
        wrappers, compiled_fn, aot_config, runtime_metadata=fw_metadata
    )
    return compiled_fn

