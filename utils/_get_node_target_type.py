
def _get_node_target_type(node: Node, gm: GraphModule) -> NSNodeTargetType | None:
    if node.op in ("call_function", "call_method"):
        return node.target
    elif node.op == "call_module":
        if not isinstance(node.target, str):
            raise AssertionError(f"Expected str, got {type(node.target)}")
        mod = getattr_from_fqn(gm, node.target)
        return type(mod)
    return None

