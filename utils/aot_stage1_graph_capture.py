
def aot_stage1_graph_capture(
    aot_state: AOTState,
    orig_flat_fn: FlatFn,
) -> AOTGraphCapture:
    # NB: flat_fn at this point coincides with the initial info from forward
    # metadata collection returning a list[Tensor].  We are now going to
    # augment the output to return a tuple[list[Tensor], list[AOTOutput]] and
    # then preserve this convention through the rest of the passes.

    # TODO: We could test for consistency with fw_metadata, but this is not a
    # big deal
    @simple_wraps(orig_flat_fn)
    def orig_flat_fn2(*args: FxValue) -> tuple[list[FxValue], list[AOTOutput]]:
        out = orig_flat_fn(*args)
        out_descs: list[AOTOutput] = type(out)(  # type: ignore[assignment]
            PlainAOTOutput(i)  # type: ignore[misc]
            for i in range(len(out))  # type: ignore[misc]
        )
        return out, out_descs

    aot_config = aot_state.aot_config

    wrappers = _create_wrappers_for_dispatch(aot_state.needs_autograd)
    flat_fn, aot_state.flat_args, aot_state.flat_args_descs, aot_state.fw_metadata = (
        pre_compile(
            wrappers,
            orig_flat_fn2,
            aot_state.flat_args,
            aot_state.flat_args_descs,
            aot_config,
            fw_metadata=aot_state.fw_metadata,
        )
    )

    # NB: This is currently only used for backwards, where fwd/bwd
    # deterministic TLS can be different
    aot_state.fw_metadata.deterministic = torch.are_deterministic_algorithms_enabled()
    updated_flat_args: list[Any] | tuple[list[Any], list[Any]]

    with maybe_skip_decompose(aot_config):
        # if config.selective_decompose, skip decomposition and apply selective_decompose
        # after we get the joint graph. See [Note: Selective Decomposition] for details.
        if aot_state.needs_autograd and not aot_config.pre_dispatch:
            # FYI: this being moved to trigger in export is new, seems fine!
            with dynamo_timed("aot_trace_joint_graph", log_pt2_compile_event=True):
                (
                    graph,
                    updated_flat_args,
                    updated_flat_args_descs,
                    maybe_subclass_meta,
                ) = aot_dispatch_autograd_graph(
                    flat_fn,
                    aot_state.flat_args,
                    aot_state.flat_args_descs,
                    aot_config,
                    fw_metadata=aot_state.fw_metadata,
                )
        else:
            graph, updated_flat_args, updated_flat_args_descs, maybe_subclass_meta = (
                aot_dispatch_base_graph(
                    flat_fn,
                    aot_state.flat_args,
                    aot_state.flat_args_descs,
                    aot_config,
                    fw_metadata=aot_state.fw_metadata,
                )
            )
            # Apply AC rematerialization to forward+loss+bwd graph
            if torch._functorch.config.remat_using_tags_for_fwd_loss_bwd_graph:
                from torch._functorch._activation_checkpointing.remat_using_tags_for_fwd_loss_bwd_graph_pass import (
                    remat_using_tags_for_fwd_loss_bwd_graph,
                )

                graph = remat_using_tags_for_fwd_loss_bwd_graph(graph)

    if config.selective_decompose:
        from torch.fx.experimental.proxy_tensor import selective_decompose
        from torch.fx.passes.regional_inductor import _needs_inductor_compile

        graph = selective_decompose(
            graph,
            *updated_flat_args,
            decomposition=aot_config.decompositions,
            should_decompose=_needs_inductor_compile,
            trace_joint_graph=aot_state.needs_autograd and not aot_config.pre_dispatch,
        )

    return AOTGraphCapture(
        wrappers=wrappers,
        graph_module=graph,
        updated_flat_args=updated_flat_args,
        updated_flat_args_descs=updated_flat_args_descs,
        maybe_subclass_meta=maybe_subclass_meta,
    )

