from typing import Any, Callable

def _prepare_graph_capture_tracing(
    fn_to_trace: Callable[..., Any],
    flat_args: Any,
    flat_args_descs: Any,
    flat_fn: TraceFn,
    *,
    fw_metadata: ViewAndMutationMeta,
    aot_config: AOTConfig,
    trace_joint: bool,
    joint_fn_handle: Any | None = None,
) -> _GraphCaptureTracingResult:
    if aot_config.disable_functionalization:
        updated_flat_args, updated_flat_args_descs = flat_args, flat_args_descs
    else:
        fn_to_trace, updated_flat_args, updated_flat_args_descs = (
            create_functionalized_fn(
                fn_to_trace,
                flat_args,
                flat_args_descs,
                meta=fw_metadata,
                aot_config=aot_config,
                trace_joint=trace_joint,
                joint_fn_handle=joint_fn_handle,
            )
        )

    subclass_tracing_info = aot_dispatch_subclass(
        fn_to_trace,
        updated_flat_args,
        updated_flat_args_descs,
        is_joint_structure=trace_joint,
        meta=fw_metadata,
        fw_only=flat_fn,
    )
    fn_to_trace = subclass_tracing_info.plain_tensor_trace_fn
    updated_flat_args = subclass_tracing_info.plain_tensor_args
    updated_flat_args_descs = subclass_tracing_info.plain_tensor_args_descs

    if not aot_config.disable_functionalization:
        fn_to_trace, updated_flat_args, updated_flat_args_descs = (
            handle_effect_tokens_fn(
                fn_to_trace,
                updated_flat_args,
                updated_flat_args_descs,
                meta=fw_metadata,
                trace_joint=trace_joint,
            )
        )

    return _GraphCaptureTracingResult(
        fn_to_trace=fn_to_trace,
        flat_args=updated_flat_args,
        flat_args_descs=updated_flat_args_descs,
        maybe_subclass_meta=subclass_tracing_info.maybe_subclass_meta,
    )

