import copy

def import_statement(
    import_start: str,
    from_imports: list[str],
    comments: Sequence[str] = (),
    line_separator: str = "\n",
    config: Config = DEFAULT_CONFIG,
    multi_line_output: Modes | None = None,
    explode: bool = False,
) -> str:
    """Returns a multi-line wrapped form of the provided from import statement."""
    if explode:
        formatter = vertical_hanging_indent
        line_length = 1
        include_trailing_comma = True
    else:
        formatter = formatter_from_string((multi_line_output or config.multi_line_output).name)
        line_length = config.wrap_length or config.line_length
        include_trailing_comma = config.include_trailing_comma
    dynamic_indent = " " * (len(import_start) + 1)
    indent = config.indent
    statement = formatter(
        statement=import_start,
        imports=copy.copy(from_imports),
        white_space=dynamic_indent,
        indent=indent,
        line_length=line_length,
        comments=comments,
        line_separator=line_separator,
        comment_prefix=config.comment_prefix,
        include_trailing_comma=include_trailing_comma,
        remove_comments=config.ignore_comments,
    )
    if config.balanced_wrapping:
        lines = statement.split(line_separator)
        line_count = len(lines)
        if len(lines) > 1:
            minimum_length = min(len(line) for line in lines[:-1])
        else:
            minimum_length = 0
        new_import_statement = statement
        while len(lines[-1]) < minimum_length and len(lines) == line_count and line_length > 10:
            statement = new_import_statement
            line_length -= 1
            new_import_statement = formatter(
                statement=import_start,
                imports=copy.copy(from_imports),
                white_space=dynamic_indent,
                indent=indent,
                line_length=line_length,
                comments=comments,
                line_separator=line_separator,
                comment_prefix=config.comment_prefix,
                include_trailing_comma=include_trailing_comma,
                remove_comments=config.ignore_comments,
            )
            lines = new_import_statement.split(line_separator)
    if statement.count(line_separator) == 0:
        return _wrap_line(statement, line_separator, config)
    return statement

