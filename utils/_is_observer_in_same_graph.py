
def _is_observer_in_same_graph(
    node: Node,
    named_modules: dict[str, torch.nn.Module],
    obs_or_fq_map: dict[EdgeOrNode, ObserverOrFakeQuantize],
    is_qat,
):
    """Check if observer in same graph
    when the node output is not fp32 and input is 'placeholder'
    the input is assumed to be quantized, so it is observed
    in a different place rather than not observed.
    """
    node_output_dtype = _get_arg_target_dtype_as_output(
        node, named_modules, obs_or_fq_map, is_qat
    )
    if len(node.args) > 0 and isinstance(node.args[0], Node):
        if (
            node_output_dtype in [torch.quint8, torch.uint8]
            and node.args[0].op == "placeholder"
        ):
            return False
    return True

