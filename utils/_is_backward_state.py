
def _is_backward_state(node: fx.Node) -> bool:
    return node.op == "placeholder" and isinstance(node.meta.get("val"), BackwardState)

