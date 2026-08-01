
def _aot_export_joint_with_descriptors(
    stack,
    mod,
    args,
    *,
    kwargs,
    decompositions,
    fake_params_buffers,
    _record_nn_module_stack=True,
):
    from torch._functorch._aot_autograd.graph_compile import aot_stage2_export
    from torch._functorch._aot_autograd.input_output_analysis import (
        create_graph_signature,
    )

    joint_with_descriptors = aot_export_joint_with_descriptors(
        stack,
        mod,
        args,
        kwargs=kwargs,
        decompositions=decompositions,
        _record_nn_module_stack=_record_nn_module_stack,
    )
    # Convert JointWithDescriptors to graph module and ViewAndMutationMeta
    gm, fw_metadata = aot_stage2_export(
        joint_with_descriptors._aot_state,
        joint_with_descriptors._aot_graph_capture,
    )

    if not isinstance(gm, torch.fx.GraphModule):
        raise AssertionError(f"expected gm to be torch.fx.GraphModule, got {type(gm)}")

    # Create GraphSignature from the metadata
    graph_signature = create_graph_signature(
        gm,
        fw_metadata,
        joint_with_descriptors.in_spec,
        joint_with_descriptors.out_spec,
        user_args_flat=pytree.tree_leaves((args, kwargs)),
        params_and_buffers_flat=list(fake_params_buffers.values()),
        param_names=joint_with_descriptors.params_spec,
        buffer_names=joint_with_descriptors.buffers_spec,
        trace_joint=False,
        num_user_fw_outs=None,
        loss_index=None,
    )
    return gm, graph_signature

