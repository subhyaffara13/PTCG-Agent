
def get_conv_fun_weight(node: Node, gm: GraphModule) -> torch.Tensor:
    # traverse backwards from the weight arg, accounting for any observers
    weight_arg_node = node.args[1]
    if not isinstance(weight_arg_node, Node):
        raise AssertionError(f"Expected Node, got {type(weight_arg_node)}")
    weight_node = return_first_non_observer_node(weight_arg_node, gm)
    if not isinstance(weight_node, Node):
        raise AssertionError(f"Expected Node, got {type(weight_node)}")
    if weight_node.op != "get_attr":
        raise AssertionError(f"Expected get_attr, got {weight_node.op}")
    weight = getattr_from_fqn(gm, weight_node.target)  # type: ignore[arg-type]
    return weight.detach()

