
def _get_decorator_optional_bool_argument(
    ctx: mypy.plugin.ClassDefContext, name: str, default: bool | None = None
) -> bool | None:
    """Return the Optional[bool] argument for the decorator.

    This handles both @decorator(...) and @decorator.
    """
    if isinstance(ctx.reason, CallExpr):
        attr_value = _get_argument(ctx.reason, name)
        if attr_value:
            if isinstance(attr_value, NameExpr):
                if attr_value.fullname == "builtins.True":
                    return True
                if attr_value.fullname == "builtins.False":
                    return False
                if attr_value.fullname == "builtins.None":
                    return None
            ctx.api.fail(
                f'"{name}" argument must be a True, False, or None literal',
                ctx.reason,
                code=LITERAL_REQ,
            )
            return default
        return default
    else:
        return default

