
def get_arg_indices_of_inputs_to_log(node: Node) -> list[int]:
    """
    Returns the indices of args of the node which we should attach
    loggers to, if input logging is enabled.

    For example,
    * for (x + y), returns [0, 1]
    * for (1 + y), returns [1]
    * for (x + 1), returns [0]
    * for (linear(x, w, b)) returns [0]
    * by default, returns [0]
    """
    if len(node.args) == 0:
        return []
    if node.op == "call_function" and (
        # TODO(future PR): use relationship map instead of hardcoding
        node.target in (torch.add, torch.ops.quantized.add, operator.add)
        or node.target in (torch.mul, torch.ops.quantized.mul, operator.mul)
    ):
        result = [i for i in range(2) if type(node.args[i]) is Node]
        return result
    return [0]

