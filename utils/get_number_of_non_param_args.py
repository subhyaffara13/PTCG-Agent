
def get_number_of_non_param_args(
    node: Node,
    gm: GraphModule,
) -> int:
    """
    Assumes that all non-param args occur first. Returns the number of
    non-param args expected for a node.  For example, for

      F.linear(x, weight, bias)

    Returns 1, because x is a non-param arg and weight and bias are params.
    For

      lstm_mod(x, hid)

    Returns 2, because both x and hid are non-param args.
    """
    if node.op == "call_module":
        node_obj = getattr_from_fqn(gm, node.target)  # type: ignore[arg-type]
        if isinstance(node_obj, nn.LSTM):
            return 2

    # default is 1
    return 1

