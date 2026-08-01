
def _no_context_variadic_positional(node: nodes.Call, scope: nodes.Lambda) -> bool:
    variadics = node.starargs + node.kwargs
    return _no_context_variadic(node, scope.args.vararg, nodes.Starred, variadics)

