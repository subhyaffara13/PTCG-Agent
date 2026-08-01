
def aot_stage2_inference(
    aot_state: AOTState,
    aot_graph_capture: AOTGraphCapture,
) -> DispatchReturn:
    """
    Handles functions that don't need autograd. Runs wrappers and compiles with fw_compiler.
    """

    aot_config = aot_state.aot_config
    fw_metadata = aot_state.fw_metadata
    fw_module = aot_graph_capture.graph_module
    wrappers = aot_graph_capture.wrappers
    updated_flat_args = aot_graph_capture.updated_flat_args
    maybe_subclass_meta = aot_graph_capture.maybe_subclass_meta

    CompileEventLogger.try_add_pt2_compile("backend_compile", dispatch_mode="inference")
    aot_forward_graph_str = _log_inference_graph(fw_module, aot_config)

    if not isinstance(fw_module, GraphModule):
        raise AssertionError(
            f"expected fw_module to be GraphModule, got {type(fw_module)}"
        )
    _apply_tensorify_python_scalars(fw_module)

    compiled_fw = _aot_stage2b_inference_compile(
        fw_module,
        updated_flat_args,  # type: ignore[arg-type]
        maybe_subclass_meta,
        fw_metadata,
        aot_config,
    )

    entry = _cache_inference_info(
        aot_config,
        fw_metadata,
        maybe_subclass_meta,
        compiled_fw,
        aot_forward_graph_str,
        wrappers,
    )

    return _aot_stage2c_make_inference_function(
        aot_config,
        fw_metadata,
        compiled_fw,
        wrappers,
        entry,
    )

