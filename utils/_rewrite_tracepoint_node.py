
def _rewrite_tracepoint_node(gm: torch.fx.GraphModule):
    """
    In-place modify input graph module by replacing the export tracepoint with a new node
    that has the same target and args, but with the _export_root stripped from path.
    """
    for node in gm.graph.nodes:
        if node.target is torch.ops.higher_order._export_tracepoint:
            if "path" in node.kwargs:
                path = _strip_root(node.kwargs["path"])
                with gm.graph.inserting_before(node):
                    new_node = gm.graph.create_node(
                        "call_function",
                        torch.ops.higher_order._export_tracepoint,
                        args=node.args,
                        kwargs={
                            "path": path,
                            "kind": node.kwargs["kind"],
                        },
                    )
                    new_node.meta = node.meta
                    node.replace_all_uses_with(new_node)
                    gm.graph.erase_node(node)

