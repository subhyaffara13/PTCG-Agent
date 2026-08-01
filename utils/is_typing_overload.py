
def is_typing_overload(value, scope_stack):
    return (
        isinstance(value.source, (ast.FunctionDef, ast.AsyncFunctionDef)) and
        any(
            _is_typing(dec, 'overload', scope_stack)
            for dec in value.source.decorator_list
        )
    )

