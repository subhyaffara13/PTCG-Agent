
def _transform_op_where_last_two_arguments_are_scale_and_zero_point(
    gm: torch.fx.GraphModule, node: torch.fx.Node
):
    """
    This transformation function can be used for function where the last two
    parameters are scale and zero point. Additionally, the function's parameters
    do not need any unpacking.
    """
    to_standard_op = {
        "mul": torch.ops.aten.mul,
        "mul_relu": torch.ops.aten.mul,
        "add": torch.ops.aten.add,
        "add_relu": torch.ops.aten.add,
        "softmax": torch.ops.aten.softmax,
        "cat": torch.ops.aten.cat,
        "hardswish": torch.ops.aten.hardswish,
    }

    if not isinstance(node.target, torch._ops.OpOverload):
        raise AssertionError(f"expected OpOverload, got {type(node.target).__name__}")
    opname, args = node.target._opname, node.args
    scale_node, zero_point_node = args[-2], args[-1]
    op_res_node = gm.graph.call_function(to_standard_op[opname], tuple(args[:-2]))
    return op_res_node, scale_node, zero_point_node

