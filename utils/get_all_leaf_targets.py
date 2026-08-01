
def get_all_leaf_targets(file: MypyFile) -> list[TargetInfo]:
    """Return all leaf targets in a symbol table (module-level and methods)."""
    result: list[TargetInfo] = []
    for fullname, node, active_type in file.local_definitions():
        if isinstance(node.node, (FuncDef, OverloadedFuncDef, Decorator)):
            result.append((fullname, node.node, active_type))
    return result

