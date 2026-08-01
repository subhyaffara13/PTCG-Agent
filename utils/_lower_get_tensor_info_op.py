
def _lower_get_tensor_info_op(model: GraphModule):
    """Modified the graph of the model inplace, to skip extra dequantize op before
    the general tensor shape ops when possible
    """
    for n in model.graph.nodes:
        if not is_get_tensor_info_node(n):
            continue
        maybe_dq = n.args[0]
        if maybe_dq.op != "call_method" or maybe_dq.target != "dequantize":
            continue
        # skip the dequantize node
        args = list(n.args)
        args[0] = n.args[0].args[0]
        n.args = tuple(args)

