
def fwd_only(
    fn: Callable[..., Any],
    args: Sequence[Any],
    *,
    run_functional_passes: bool = True,
    get_decomp_fn: Callable[..., Any] = select_decomp_table,
) -> torch.fx.GraphModule:
    """Build a normalized inference graph, for use with fx_to_pattern"""
    # TODO - look into using aot autograd, asserting no mutating ops here
    with enable_python_dispatcher(), preserve_node_meta():
        gm = make_fx(fn, get_decomp_fn(), tracing_mode="real")(*args)

    from .fx_passes.post_grad import remove_noop_ops

    if run_functional_passes:
        remove_noop_ops(gm.graph)

        # NOTE: applying early_patterns to user patterns cause
        # duplicate patterns being found in vllm. Check
        # https://github.com/pytorch/pytorch/pull/170649#issuecomment-3693427775
        # for more details.
        # from .fx_passes.joint_graph import early_patterns
        # early_patterns.apply(gm.graph)

        gm.graph.eliminate_dead_code()

    gm.recompile()
    return gm

