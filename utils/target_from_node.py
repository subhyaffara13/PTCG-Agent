
def target_from_node(module: str, node: FuncDef | MypyFile | OverloadedFuncDef) -> str | None:
    """Return the target name corresponding to a deferred node.

    Args:
        module: Must be module id of the module that defines 'node'

    Returns the target name, or None if the node is not a valid target in the given
    module (for example, if it's actually defined in another module).
    """
    if isinstance(node, MypyFile):
        if module != node.fullname:
            # Actually a reference to another module -- likely a stale dependency.
            return None
        return module
    else:  # OverloadedFuncDef or FuncDef
        if node.info:
            return f"{node.info.fullname}.{node.name}"
        else:
            return f"{module}.{node.name}"

