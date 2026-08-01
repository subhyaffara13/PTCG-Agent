
def format_inline_array(obj: tuple | list, ctx: Context, nest_level: int) -> str:
    if not obj:
        return "[]"
    item_indent = ctx.indent_str * (1 + nest_level)
    closing_bracket_indent = ctx.indent_str * nest_level
    return (
        "[\n"
        + ",\n".join(
            item_indent + format_literal(item, ctx, nest_level=nest_level + 1)
            for item in obj
        )
        + f",\n{closing_bracket_indent}]"
    )


def format_inline_array(obj: tuple | list, ctx: Context, nest_level: int) -> str:
    if not obj:
        return "[]"
    item_indent = ctx.indent_str * (1 + nest_level)
    closing_bracket_indent = ctx.indent_str * nest_level
    return (
        "[\n"
        + ",\n".join(
            item_indent + format_literal(item, ctx, nest_level=nest_level + 1)
            for item in obj
        )
        + f",\n{closing_bracket_indent}]"
    )

