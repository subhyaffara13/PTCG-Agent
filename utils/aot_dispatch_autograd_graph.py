
def aot_dispatch_autograd_graph(
    flat_fn: TraceFn,
    flat_args: list[Any],
    flat_args_descs: list[AOTInput],
    aot_config: AOTConfig,
    *,
    fw_metadata: ViewAndMutationMeta,
) -> tuple[
    torch.fx.GraphModule,
    tuple[list[Any], list[Any]],
    tuple[list[AOTInput], list[AOTInput]],
    SubclassMeta | None,
]:
    # NB: flat_fn here is the original user function (as far as
    # aot_module_simplified is concerned)

    # traced_tangents corresponds to the set of outputs in the traced forward that should get grad_outputs in the traced backward.
    # It includes outputs of the original forward, *and* any updated inputs due to input mutations.
    # However, it does *not* include any outputs that are aliases of inputs or intermediates, or any metadata-only input mutations.
    joint_inputs = (flat_args, fw_metadata.traced_tangents)
    joint_inputs_descs = (flat_args_descs, fw_metadata.traced_tangents_descs)

    fn_prepared_for_autograd = fn_prepped_for_autograd(
        flat_fn,
        flat_args_descs,
        fw_metadata,
        aot_config,
    )
    joint_fn_to_trace = create_joint(
        fn_prepared_for_autograd, flat_args_descs, aot_config=aot_config
    )
    # pyrefly: ignore[missing-attribute]
    joint_fn_handle = joint_fn_to_trace.handle
    # TODO: replace with AOTDispatchSubclassWrapper once we refactor
    # fn_input_mutations_to_outputs and create_functionalized_fn
    # into CompilerWrappers.
    tracing_state = _prepare_graph_capture_tracing(
        joint_fn_to_trace,
        joint_inputs,
        joint_inputs_descs,
        flat_fn,
        fw_metadata=fw_metadata,
        aot_config=aot_config,
        trace_joint=True,
        joint_fn_handle=joint_fn_handle,
    )
    joint_fn_to_trace = tracing_state.fn_to_trace
    updated_joint_inputs = tracing_state.flat_args
    updated_joint_inputs_descs = tracing_state.flat_args_descs
    maybe_subclass_meta = tracing_state.maybe_subclass_meta

    # When we call _create_graph, this may mutate the metadata of joint
    # inputs.  But callers are expecting to get the original joint inputs.  So
    # we make aliases of all the inputs to make sure we have a copy that
    # doesn't get modified.
    #
    # This destroys requires_grad/grad_fn information.  However, backends
    # beneath AOTAutograd are indifferent to this information, so it doesn't
    # matter.
    fx_g, saved_updated_joint_inputs = _create_graph_and_save_traced_inputs(
        joint_fn_to_trace,
        updated_joint_inputs,
        updated_joint_inputs_descs,
        aot_config=aot_config,
    )

    # Redundant with the check above, but worth having in case tracing introduced
    # a fake tensor. Unlikely.
    # See Note: [Fake Modules and AOTAutograd]
    torch._dynamo.utils.assert_no_fake_params_or_buffers(fx_g)

    # Have to copy before eliminate_dead_code otherwise the
    # fw node match might be erased
    copy_fwd_metadata_to_bw_nodes(fx_g)

    # After copying metadata, assign streams to gradient accumulation nodes
    assign_backward_streams(fx_g)

    assign_epilogue_copy_streams(fx_g)

    # Insert syncs for newly assigned backward streams
    insert_backward_syncs(fx_g)

    # Sync deallocations for tensors where the stream w/ their last usage
    # is distinct from their allocation stream
    sync_deallocations(fx_g)

    # Wrap sync nodes with control_deps to prevent reordering
    # (must be after sync_deallocations which inserts additional sync nodes)
    wrap_all_sync_nodes_with_control_deps(fx_g)

    # Populate fw_metadata with stream indices from the compiled graph
    # NB: This needs to be done after the above stream assignments
    populate_fw_metadata_with_stream_indices(fx_g, fw_metadata)

    # this helps users identify which forward output to call .detach() on.
    _extract_tangent_source_stack_traces(fx_g, fw_metadata)

    fx_g.graph.eliminate_dead_code()
    if not aot_config.disable_functionalization:
        # There should be *NO* mutating ops in the graph at this point.
        assert_functional_graph(fx_g.graph)

    fx_g.recompile()

    # TODO: in AOTAutograd, we create metadata like _indices_of_inps_to_detach to detect
    # when we need to manually detach() some inputs in the forward.
    # Higher order ops might eventually need to do the same.
    if aot_config.is_export and maybe_subclass_meta is not None:
        raise AssertionError(
            "aot_export_module does not support tensor subclass inputs for now."
        )
    return (
        fx_g,
        saved_updated_joint_inputs,
        updated_joint_inputs_descs,
        maybe_subclass_meta,
    )

