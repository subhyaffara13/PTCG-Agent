from typing import Any

def node_arg_is_weight(node: Node, arg: Any) -> bool:
    """Returns if node arg is weight"""
    weight_index = None
    if "target_dtype_info" in node.meta:
        weight_index = node.meta["target_dtype_info"].get("weight_index", None)
    if (
        weight_index is not None
        and weight_index < len(node.args)
        and node.args[weight_index] is arg
    ):
        return True
    return node.kwargs.get("weight") is arg

