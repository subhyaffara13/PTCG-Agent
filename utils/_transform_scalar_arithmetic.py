
def _transform_scalar_arithmetic(gm: torch.fx.GraphModule, node: torch.fx.Node):
    """Transform scalar overload for basic arithmetic."""
    to_standard_op = {
        "mul": torch.ops.aten.mul.Scalar,
        "add": torch.ops.aten.add.Scalar,
    }
    if not isinstance(node.target, torch._ops.OpOverload):
        raise AssertionError(f"expected OpOverload, got {type(node.target).__name__}")
    opname, args = node.target._opname, node.args
    op_res_node = gm.graph.call_function(to_standard_op[opname], args)
    return op_res_node, _SCALE, _ZERO_POINT

