
def require_bool_literal_argument(
    api: SemanticAnalyzerInterface | SemanticAnalyzerPluginInterface,
    expression: Expression,
    name: str,
    default: Literal[True, False],
) -> bool: ...


def require_bool_literal_argument(
    api: SemanticAnalyzerInterface | SemanticAnalyzerPluginInterface,
    expression: Expression,
    name: str,
    default: None = None,
) -> bool | None: ...


def require_bool_literal_argument(
    api: SemanticAnalyzerInterface | SemanticAnalyzerPluginInterface,
    expression: Expression,
    name: str,
    default: bool | None = None,
) -> bool | None:
    """Attempt to interpret an expression as a boolean literal, and fail analysis if we can't."""
    value = parse_bool(expression)
    if value is None:
        api.fail(
            f'"{name}" argument must be a True or False literal', expression, code=LITERAL_REQ
        )
        return default

    return value

