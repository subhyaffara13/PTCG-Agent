
def _parse_expression(expr: str, exc_message: str) -> Expression:
    try:
        return Expression.compile(expr)
    except SyntaxError as e:
        raise UsageError(
            f"{exc_message}: {e.text}: at column {e.offset}: {e.msg}"
        ) from None

