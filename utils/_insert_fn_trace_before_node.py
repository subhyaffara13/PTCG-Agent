
def _insert_fn_trace_before_node(  # type: ignore[no-untyped-def]
    g: torch.fx.Graph,
    fn_to_trace,
    inps,
    insert_before_node: torch.fx.Node,
    g_fn_inps: list[torch.fx.Node],
    g_fn_outs: list[torch.fx.Node],
) -> tuple[dict[torch.fx.Node, torch.fx.Node], list[torch.fx.Node]]:  # type: ignore[no-untyped-def]
    """
    Helper function that traces :attr:`fn_to_trace` with inputs
    :attr:`inps`.
    The result function graph will be inserted before :attr:`insert_before_node`,
    using :attr:`g_fn_inps` nodes of original graph as inputs of function graph,
    function graph outputs will replace :attr:`g_fn_outs` in original graph.

    Returns:
        (replacements, new_nodes): Dictionary mapping old to new nodes, and list of all newly inserted nodes
    """
    with dynamo_timed(
        "fx.bucketing._insert_fn_trace_before_node", log_pt2_compile_event=True
    ):
        fn_gm = _trace(
            fn_to_trace,
            inps,
        )
        fn_g = fn_gm.graph
        fn_g_ins = fn_g.find_nodes(op="placeholder")
        env = {fn_g_ins[idx]: g_fn_inps[idx] for idx in range(len(g_fn_inps))}
        g_fn_new_outs: list[torch.fx.Node] = []
        new_nodes: list[torch.fx.Node] = []  # Track all newly inserted nodes

        with g.inserting_before(insert_before_node):
            for _n in fn_g.nodes:
                if _n.op == "placeholder":
                    continue
                _new_n = g.node_copy(_n, lambda x: env[x])
                env[_n] = _new_n
                if _n.op == "output":
                    g_fn_new_outs = _new_n.args[0]  # type: ignore[assignment]
                    g.erase_node(_new_n)
                else:
                    new_nodes.append(_new_n)  # Track non-output nodes

        replacements = {  # noqa: C416
            orig_out: new_out for orig_out, new_out in zip(g_fn_outs, g_fn_new_outs)
        }
        for orig_out, new_out in zip(g_fn_outs, g_fn_new_outs):
            orig_out.replace_all_uses_with(new_out)

        return replacements, new_nodes

