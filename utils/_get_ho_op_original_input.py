
def _get_ho_op_original_input(getitem_node: fx.Node) -> fx.Node | None:
    """Given a getitem node, check if it extracts from a higher-order op
    that has kwargs mapping the key back to an original input.

    Returns the original input node if found, None otherwise.
    """
    if getitem_node.target != operator.getitem:
        return None
    ho_result = getitem_node.args[0]
    key = getitem_node.args[1]
    if not isinstance(ho_result, fx.Node) or ho_result.op != "call_function":
        return None
    if "kwargs" not in ho_result.kwargs:
        return None
    kwargs = ho_result.kwargs["kwargs"]
    # pyrefly: ignore [not-iterable, unsupported-operation]
    if key not in kwargs:
        return None
    # pyrefly: ignore [bad-index, unsupported-operation]
    original_input = kwargs[key]
    if isinstance(original_input, fx.Node):
        return original_input
    return None

