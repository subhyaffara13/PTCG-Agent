
def resolve_to_class_def(types: set[nodes.NodeNG]) -> set[nodes.ClassDef]:
    """Resolve a set of nodes to ClassDef nodes."""
    class_defs = set()
    for node in types:
        if isinstance(node, nodes.ClassDef):
            class_defs.add(node)
        elif isinstance(node, nodes.Name):
            inferred = safe_infer(node)
            if isinstance(inferred, nodes.ClassDef):
                class_defs.add(inferred)
        elif isinstance(node, astroid.Instance):
            # Instance of a class -> get the actual class
            class_defs.add(node._proxied)
    return class_defs

