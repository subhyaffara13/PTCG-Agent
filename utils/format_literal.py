
def format_literal(obj: object, ctx: Context, *, nest_level: int = 0) -> str:
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float, date, datetime)):
        return str(obj)
    if isinstance(obj, time):
        if obj.tzinfo:
            raise ValueError("TOML does not support offset times")
        return str(obj)
    if isinstance(obj, str):
        return format_string(obj, allow_multiline=ctx.allow_multiline)
    if isinstance(obj, ARRAY_TYPES):
        return format_inline_array(obj, ctx, nest_level)
    if isinstance(obj, Mapping):
        return format_inline_table(obj, ctx)

    # Lazy import to improve module import time
    from decimal import Decimal

    if isinstance(obj, Decimal):
        return format_decimal(obj)
    raise TypeError(
        f"Object of type '{type(obj).__qualname__}' is not TOML serializable"
    )


def format_literal(obj: object, ctx: Context, *, nest_level: int = 0) -> str:
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float, date, datetime)):
        return str(obj)
    if isinstance(obj, time):
        if obj.tzinfo:
            raise ValueError("TOML does not support offset times")
        return str(obj)
    if isinstance(obj, str):
        return format_string(obj, allow_multiline=ctx.allow_multiline)
    if isinstance(obj, ARRAY_TYPES):
        return format_inline_array(obj, ctx, nest_level)
    if isinstance(obj, Mapping):
        return format_inline_table(obj, ctx)

    # Lazy import to improve module import time
    from decimal import Decimal

    if isinstance(obj, Decimal):
        return format_decimal(obj)
    raise TypeError(
        f"Object of type '{type(obj).__qualname__}' is not TOML serializable"
    )

