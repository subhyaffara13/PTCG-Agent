from typing import Any

def node_arg_is_bias(node: Node, arg: Any) -> bool:
    """Returns if node arg is bias"""
    bias_index = None
    if "target_dtype_info" in node.meta:
        bias_index = node.meta["target_dtype_info"].get("bias_index", None)
    if (
        bias_index is not None
        and bias_index < len(node.args)
        and node.args[bias_index] is arg
    ):
        return True
    return node.kwargs.get("bias") is arg

