
def get_non_observable_arg_indexes_and_types(
    node: Node,
) -> dict[type | torch.dtype, Callable[[Node], list[int]]]:
    """
    Returns a dict with of non float tensor types as keys and values which correspond to a
    function to retrieve the list (which takes the node as an argument)
    """
    info = NodeInfo(node.op, node.target)

    return NON_OBSERVABLE_ARG_DICT.get(info, EMPTY_ARG_DICT)

