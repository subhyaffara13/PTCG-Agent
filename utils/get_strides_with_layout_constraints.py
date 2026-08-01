
def get_strides_with_layout_constraints(node):
    if (
        not isinstance(node, ir.ReinterpretView)
        and node.get_name() in V.graph.buffer_layout_constraints
    ):
        return V.graph.buffer_layout_constraints[node.get_name()].stride
    return node.get_stride()

