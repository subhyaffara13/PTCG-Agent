
def aot_stage2_autograd(
    aot_state: AOTState,
    aot_graph_capture: AOTGraphCapture,
) -> DispatchReturn:
    """
    Autograd logic. Generates a joint graph, partitions it, manipulates the input with various wrappers,
    and returns a wrapped torch.autograd.Function with a forward and backward.
    """

    fx_g = aot_graph_capture.graph_module
    maybe_subclass_meta = aot_graph_capture.maybe_subclass_meta
    fw_metadata = aot_state.fw_metadata
    aot_config = aot_state.aot_config

    CompileEventLogger.try_add_pt2_compile("backend_compile", dispatch_mode="autograd")
    joint_graph_str = _log_joint_graph(fx_g, aot_config)

    _apply_tensorify_python_scalars(fx_g)

    (
        fw_module,
        bw_module,
        num_fw_outs_saved_for_bw,
        num_symints_saved_for_bw,
        _indices_of_inps_to_detach,
        adjusted_flat_args,
    ) = _aot_stage2a_partition(
        fx_g,
        aot_graph_capture.updated_flat_args,
        maybe_subclass_meta,
        fw_metadata,
        aot_config,
    )

    fw_module_str, bw_module_str = _log_fw_bw_graphs(
        fw_module, bw_module, maybe_subclass_meta, fw_metadata, aot_config
    )

    fwd_output_strides, compiled_fw_func = _aot_stage2b_fw_compile(
        fw_module,
        adjusted_flat_args,
        maybe_subclass_meta,
        fw_metadata,
        num_fw_outs_saved_for_bw,
        aot_config,
    )

    lazy_backward_info, compiled_bw_func = _aot_stage2b_bw_compile(
        bw_module,
        maybe_subclass_meta,
        fw_metadata,
        fwd_output_strides,
        num_symints_saved_for_bw,
        aot_config,
    )

    try_save_cache_entry, entry = _cache_autograd_info(
        aot_config,
        aot_state.flat_args,
        compiled_fw_func,
        compiled_bw_func,
        fw_module_str,
        bw_module_str,
        joint_graph_str,
        aot_graph_capture.wrappers,
        maybe_subclass_meta,
        fw_metadata,
        num_fw_outs_saved_for_bw,
        _indices_of_inps_to_detach,
        num_symints_saved_for_bw,
        bw_module,
    )

    return _aot_stage2c_make_autograd_function(
        aot_config,
        aot_state.flat_args,
        fw_metadata,
        maybe_subclass_meta,
        aot_graph_capture.wrappers,
        compiled_fw_func,
        compiled_bw_func,
        lazy_backward_info,
        try_save_cache_entry,  # type: ignore[arg-type]
        entry,  # type: ignore[arg-type]
        _indices_of_inps_to_detach,
        num_symints_saved_for_bw,
    )

