
def _builtin_filter_predicate(node, builtin_name) -> bool:
    # pylint: disable = too-many-boolean-expressions
    if (
        builtin_name == "type"
        and node.root().name == "re"
        and isinstance(node.func, nodes.Name)
        and node.func.name == "type"
        and isinstance(node.parent, nodes.Assign)
        and len(node.parent.targets) == 1
        and isinstance(node.parent.targets[0], nodes.AssignName)
        and node.parent.targets[0].name in {"Pattern", "Match"}
    ):
        # Handle re.Pattern and re.Match in brain_re
        # Match these patterns from stdlib/re.py
        # ```py
        # Pattern = type(...)
        # Match = type(...)
        # ```
        return False
    if isinstance(node.func, nodes.Name):
        return node.func.name == builtin_name
    if isinstance(node.func, nodes.Attribute):
        return (
            node.func.attrname == "fromkeys"
            and isinstance(node.func.expr, nodes.Name)
            and node.func.expr.name == "dict"
        )
    return False

