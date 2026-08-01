
def _no_context_variadic(
    node: nodes.Call,
    variadic_name: str | None,
    variadic_type: nodes.Keyword | nodes.Starred,
    variadics: list[nodes.Keyword | nodes.Starred],
) -> bool:
    """Verify if the given call node has variadic nodes without context.

    This is a workaround for handling cases of nested call functions
    which don't have the specific call context at hand.
    Variadic arguments (variable positional arguments and variable
    keyword arguments) are inferred, inherently wrong, by astroid
    as a Tuple, respectively a Dict with empty elements.
    This can lead pylint to believe that a function call receives
    too few arguments.
    """
    scope = node.scope()
    is_in_lambda_scope = not isinstance(scope, nodes.FunctionDef) and isinstance(
        scope, nodes.Lambda
    )
    statement = node.statement()
    for name in statement.nodes_of_class(nodes.Name):
        if name.name != variadic_name:
            continue

        inferred = safe_infer(name)
        if isinstance(inferred, (nodes.List, nodes.Tuple)):
            length = len(inferred.elts)
        elif isinstance(inferred, nodes.Dict):
            length = len(inferred.items)
        else:
            continue

        if is_in_lambda_scope and isinstance(inferred.parent, nodes.Arguments):
            # The statement of the variadic will be the assignment itself,
            # so we need to go the lambda instead
            inferred_statement = inferred.parent.parent
        else:
            inferred_statement = inferred.statement()

        if not length and isinstance(
            inferred_statement, (nodes.Lambda, nodes.FunctionDef)
        ):
            is_in_starred_context = _has_parent_of_type(node, variadic_type, statement)
            used_as_starred_argument = any(
                variadic.value == name or variadic.value.parent_of(name)
                for variadic in variadics
            )
            if is_in_starred_context or used_as_starred_argument:
                return True
    return False

