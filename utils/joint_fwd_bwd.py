
def joint_fwd_bwd(
    fn: Callable[..., Any],
    args: Sequence[Any],
    *,
    get_decomp_fn: Callable[..., Any] = select_decomp_table,
) -> torch.fx.GraphModule:
    """Build a normalized training graph, for use with fx_to_pattern"""
    gm: torch.fx.GraphModule | None = None

    def record_joint_graph(
        joint_graph: torch.fx.GraphModule, inputs: Sequence[Any], **kwargs: Any
    ) -> tuple[torch.fx.GraphModule, torch.fx.GraphModule]:
        nonlocal gm
        assert not gm
        gm = clone_graph(joint_graph)
        return default_partition(joint_graph, inputs, **kwargs)

    with torch._guards.tracing(None):
        aot_function(
            fn,
            # pyrefly: ignore[bad-argument-type]
            lambda gm, example_inputs: make_boxed_func(gm),
            partition_fn=record_joint_graph,
            decompositions=get_decomp_fn(),
            keep_inference_input_mutations=True,
            enable_log=False,
        )(*args)
    assert gm

    from .fx_passes.post_grad import remove_noop_ops

    remove_noop_ops(gm.graph)

    from .fx_passes.joint_graph import early_patterns

    early_patterns.apply(gm.graph)

    # remove in/out specs
    gm.graph._codegen = torch.fx.graph.CodeGen()
    gm.graph.eliminate_dead_code()
    gm.recompile()
    return gm

