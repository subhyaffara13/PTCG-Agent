
def insert_fused_activation_node(
    gm: torch.fx.GraphModule, opname: str, fx_node: torch.fx.Node
) -> torch.fx.Node:
    if opname in ["conv1d_relu", "conv2d_relu", "linear_relu", "add_relu", "mul_relu"]:
        fx_node = gm.graph.call_function(torch.ops.aten.relu, (fx_node,))
    return fx_node

