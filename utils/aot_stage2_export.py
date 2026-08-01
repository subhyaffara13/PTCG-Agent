
def aot_stage2_export(
    aot_state: AOTState, aot_graph_capture: AOTGraphCapture
) -> DispatchReturn:
    graph = aot_graph_capture.graph_module
    aot_config = aot_state.aot_config
    wrappers = aot_graph_capture.wrappers

    CompileEventLogger.try_add_pt2_compile("backend_compile", dispatch_mode="export")

    # NB: the wrappers that run in pre_compile for export are
    # either a no-op, because they're not needed, or will raise a runtime error,
    # since they don't support export.
    # We still run these wrappers to make sure that they're not needed pre compile,
    # but we technically don't need to run them post compile at all here.
    compiled_fn, aot_state.fw_metadata = post_compile(
        wrappers,
        graph,  # pyrefly: ignore [bad-argument-type]
        aot_config,
        runtime_metadata=aot_state.fw_metadata,
    )

    # Therefore, since no wrapperes run, we don't get back a callable - we get back the raw fx graph
    # (either a joint or an inference-only graph)
    if not isinstance(compiled_fn, torch.fx.GraphModule):
        raise AssertionError(
            f"expected compiled_fn to be GraphModule, got {type(compiled_fn)}"
        )
    return compiled_fn, aot_state.fw_metadata

