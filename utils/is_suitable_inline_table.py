
def is_suitable_inline_table(obj: Mapping, ctx: Context) -> bool:
    """Use heuristics to decide if the inline-style representation is a good
    choice for a given table."""
    rendered_inline = f"{ctx.indent_str}{format_inline_table(obj, ctx)},"
    return len(rendered_inline) <= MAX_LINE_LENGTH and "\n" not in rendered_inline


def is_suitable_inline_table(obj: Mapping, ctx: Context) -> bool:
    """Use heuristics to decide if the inline-style representation is a good
    choice for a given table."""
    rendered_inline = f"{ctx.indent_str}{format_inline_table(obj, ctx)},"
    return len(rendered_inline) <= MAX_LINE_LENGTH and "\n" not in rendered_inline

