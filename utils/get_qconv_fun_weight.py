
def get_qconv_fun_weight(node: Node, gm: GraphModule) -> torch.Tensor:
    # qconv state is arg 1
    qconv_state_node = node.args[1]
    if not isinstance(qconv_state_node, Node):
        raise AssertionError(f"Expected Node, got {type(qconv_state_node)}")
    if qconv_state_node.op != "get_attr":
        raise AssertionError(f"Expected get_attr, got {qconv_state_node.op}")
    qconv_state_obj = getattr_from_fqn(gm, qconv_state_node.target)  # type: ignore[arg-type]
    return qconv_state_obj.weight()

