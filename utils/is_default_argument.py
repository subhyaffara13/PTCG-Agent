
def is_default_argument(node: nodes.NodeNG, scope: nodes.NodeNG | None = None) -> bool:
    """Return true if the given Name node is used in function or lambda
    default argument's value.
    """
    if not scope:
        scope = node.scope()
    if isinstance(scope, (nodes.FunctionDef, nodes.Lambda)):
        all_defaults = itertools.chain(
            scope.args.defaults, (d for d in scope.args.kw_defaults if d is not None)
        )
        return any(
            default_name_node is node
            for default_node in all_defaults
            for default_name_node in default_node.nodes_of_class(nodes.Name)
        )

    return False

