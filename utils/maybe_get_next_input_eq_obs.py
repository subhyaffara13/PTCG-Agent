
def maybe_get_next_input_eq_obs(
    node: Node, modules: dict[str, nn.Module]
) -> _InputEqualizationObserver | None:
    """Gets the following input equalization observer if it exists.

    For example, in the case of connecting linear layers:
        x -> inp_obs1 -> eq_obs1 -> linear1 -> out_obs1 -> eq_obs2 -> linear2 -> out_obs2
    If the node being passed in is the linear1 node, then we want to return eq_obs2,
    the following equalization observer for linear2.

    However, if there are no connecting layers:
        x -> inp_obs1 -> eq_obs1 -> linear1 -> out_obs1 -> add
    Then we want to return None.

    In the case of an unfused linear-relu layer with a connecting linear layer:
        linear1 -> relu -> out_obs1 -> eq_obs2 -> linear2 -> out_obs2
    Since it is unfused, we want to skip over the relu layer and return eq_obs2,
    the following equalization observer for linear2.
    """

    if not node_supports_equalization(node, modules):
        raise AssertionError("Node does not support equalization")

    # Locate the following nn.ReLU or F.relu node if it exists
    maybe_relu_node = maybe_get_next_module(node, modules, nn.ReLU)
    if maybe_relu_node is None:
        maybe_relu_node = maybe_get_next_module(
            node, modules, target_functional_type=F.relu
        )

    # Locate the following output observer if it exists.
    # We will skip the relu node if it exists.
    maybe_obs_node = (
        maybe_get_next_module(node, modules, ObserverBase)
        if maybe_relu_node is None
        else maybe_get_next_module(maybe_relu_node, modules, ObserverBase)
    )
    if maybe_obs_node is None:
        return None

    maybe_eq_obs_node = maybe_get_next_module(
        maybe_obs_node, modules, _InputEqualizationObserver
    )
    if maybe_eq_obs_node is None:
        return None

    maybe_eq_obs = modules[str(maybe_eq_obs_node)]
    if not isinstance(maybe_eq_obs, _InputEqualizationObserver):
        raise AssertionError(
            "Expected the following equalization observer to be an _InputEqualizationObserver"
        )
    return maybe_eq_obs

