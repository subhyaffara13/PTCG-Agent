
def _lower_getattr_tensor_metadta_op(model: GraphModule):
    """Modified the graph of the model inplace, to skip extra dequantize op before
    the general tensor shape ops when possible
    """
    for n in model.graph.nodes:
        if is_getattr_tensor_metadata_node(n):
            maybe_dq = n.args[0]
            if maybe_dq.op != "call_method" or maybe_dq.target != "dequantize":
                continue
            # skip the dequantize node
            args = list(n.args)
            args[0] = n.args[0].args[0]
            n.args = tuple(args)

