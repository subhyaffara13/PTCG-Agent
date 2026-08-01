
def _get_bool_argument(ctx: ClassDefContext, expr: CallExpr, name: str, default: bool) -> bool:
    """Return the boolean value for an argument to a call or the
    default if it's not found.
    """
    attr_value = _get_argument(expr, name)
    if attr_value:
        return require_bool_literal_argument(ctx.api, attr_value, name, default)
    return default

