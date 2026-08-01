
def trace_joint_graph_as_bwd(
    subgraph, num_primals, joint_operands, include_key_set, exclude_key_set
):
    """
    Naively trace out a joint graph. This simplifies the reconstruction of joint
    graph in the min-cut partitioner later on.
    """
    from torch._functorch.aot_autograd import create_joint

    dummy_aot_config = get_dummy_aot_autograd_config()

    if isinstance(subgraph, torch.fx.GraphModule):

        def graph_with_interpreter(*args):
            # Running graph with interpreter is needed for propagating the stack_trace
            with torch.fx.traceback.preserve_node_meta():
                return torch.fx.Interpreter(subgraph).run(*args)

        fn = graph_with_interpreter
    else:
        fn = subgraph

    # This joint_fn is inserted as the backward graph as is. This simplifies the
    # min-cut partitioner work later on.
    #   Input signature - (*primals, *tangents)
    #   Output signature - (*grads, *fw_outs)
    # The output signature is deliberately kept grads first and fw_outs second.
    # Having grads first makes the min-cut partitioner HOP graph stitching
    # easier.
    def joint_fn(*primals_and_tangents):
        primals = primals_and_tangents[:num_primals]
        tangents = primals_and_tangents[num_primals:]

        fw_outs, grads = create_joint(
            prepare_fw_with_masks(fn), aot_config=dummy_aot_config
        )(primals, tangents)

        maybe_clone = clone_outputs_aliasing_inputs(primals_and_tangents)

        # return signature is deliberately kept (*grads, *fw_outs). This
        # simplifies partitioning work later on.
        return pytree.tree_map(maybe_clone, tuple(grads + list(fw_outs)))

    with suspend_functionalization(), disable_functional_mode():
        with disable_proxy_modes_tracing():
            joint_operands = [_from_fun(arg) for arg in joint_operands]
            with contextlib.ExitStack() as stack:
                stack.enter_context(
                    torch._C._ForceDispatchKeyGuard(include_key_set, exclude_key_set),
                )
                subgraph_decomp_table = _extract_nested_region_config(subgraph)
                with torch.enable_grad():
                    return _maybe_reenter_make_fx(
                        joint_fn, subgraph_decomp_table=subgraph_decomp_table
                    )(*joint_operands)

