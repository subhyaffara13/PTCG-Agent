
def get_target_type_str(node: Node, gm: GraphModule) -> str:
    """
    Returns a string representation of the type of the function or module
    pointed to by this node, or '' for other node types.
    """
    target_type = ""
    if node.op in ("call_function", "call_method"):
        target_type = torch.typename(node.target)
    elif node.op == "call_module":
        if not isinstance(node.target, str):
            raise AssertionError(f"Expected str, got {type(node.target)}")
        target_mod = getattr_from_fqn(gm, node.target)
        target_type = torch.typename(target_mod)
    return target_type

