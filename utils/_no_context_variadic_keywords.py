
def _no_context_variadic_keywords(node: nodes.Call, scope: nodes.Lambda) -> bool:
    statement = node.statement()
    variadics = []

    if (
        isinstance(scope, nodes.Lambda) and not isinstance(scope, nodes.FunctionDef)
    ) or isinstance(statement, nodes.With):
        variadics = list(node.keywords or []) + node.kwargs
    elif isinstance(statement, (nodes.Return, nodes.Expr, nodes.Assign)) and isinstance(
        statement.value, nodes.Call
    ):
        call = statement.value
        variadics = list(call.keywords or []) + call.kwargs

    return _no_context_variadic(node, scope.args.kwarg, nodes.Keyword, variadics)

