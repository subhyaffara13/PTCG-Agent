
def _is_tangent(node: torch.fx.Node) -> bool:
    return node.op == "placeholder" and "tangents" in str(node.target)

