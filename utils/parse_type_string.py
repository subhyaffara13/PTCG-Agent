
def parse_type_string(
    expr_string: str, expr_fallback_name: str, line: int, column: int
) -> ProperType:
    """Parses a type that was originally present inside of an explicit string.

    For example, suppose we have the type `Foo["blah"]`. We should parse the
    string expression "blah" using this function.
    """
    try:
        _, node = parse_type_comment(f"({expr_string})", line=line, column=column, errors=None)
        if isinstance(node, (UnboundType, UnionType)) and node.original_str_expr is None:
            node.original_str_expr = expr_string
            node.original_str_fallback = expr_fallback_name
            return node
        else:
            return RawExpressionType(expr_string, expr_fallback_name, line, column)
    except (SyntaxError, ValueError):
        # Note: the parser will raise a `ValueError` instead of a SyntaxError if
        # the string happens to contain things like \x00.
        return RawExpressionType(expr_string, expr_fallback_name, line, column)

