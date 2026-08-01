
def _get_linear_node(match, input_dim_exceeds_two, input_contiguous):
    output_reshape_node = None
    if input_dim_exceeds_two:
        if input_contiguous:
            output_reshape_node = match.output_node()
            assert output_reshape_node.target is aten.reshape.default
            linear_node = output_reshape_node.args[0]
        else:
            linear_nodes = filter_nodes(match.nodes, aten.bmm.default)
            assert len(linear_nodes) == 1
            linear_node = linear_nodes[0]
    else:
        linear_node = match.output_node()

    assert linear_node.target in (
        aten.addmm.default,
        aten.mm.default,
        aten.bmm.default,
    )
    return linear_node, output_reshape_node

