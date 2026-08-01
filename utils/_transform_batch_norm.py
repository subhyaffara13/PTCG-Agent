
def _transform_batch_norm(gm: torch.fx.GraphModule, node: torch.fx.Node):
    args = node.args
    scale_node, zero_point_node = args[-2], args[-1]
    op_res_node = gm.graph.call_function(
        torch.ops.aten.native_batch_norm, (*args[:-3], False, 0.1, args[-3])
    )
    op_res_node = gm.graph.call_function(operator.getitem, (op_res_node, 0))
    return op_res_node, scale_node, zero_point_node

