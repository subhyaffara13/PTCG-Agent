
def enforce_as_strided_input_layout(gm: torch.fx.GraphModule):
    """
    Make sure the as_strided node's input's layout does not change due to compiler
    optimizations, because the as_strided strides info depends on input tensor stride info.
    """

    as_strided_ops = [
        torch.ops.aten.as_strided.default,
        torch.ops.aten.as_strided_.default,
        torch.ops.aten.as_strided_scatter.default,
    ]
    strided_nodes = [n for n in gm.graph.nodes if n.target in as_strided_ops]
    for n in strided_nodes:
        with gm.graph.inserting_before(n):
            # add a node to enforce eager layout
            ft = n.args[0].meta["val"]
            new_node = gm.graph.call_function(
                prims.inductor_force_stride_order.default, (n.args[0], ft.stride())
            )
            n.replace_input_with(n.args[0], new_node)

    gm.graph.lint()
    gm.recompile()

