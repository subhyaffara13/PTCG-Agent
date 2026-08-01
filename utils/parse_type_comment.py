
def parse_type_comment(
    type_comment: str, line: int, column: int, errors: Errors | None
) -> tuple[list[str] | None, ProperType | None]:
    """Parse type portion of a type comment (+ optional type ignore).

    Return (ignore info, parsed type).
    """
    try:
        typ = ast3_parse(type_comment, "<type_comment>", "eval")
    except SyntaxError:
        if errors is not None:
            stripped_type = type_comment.split("#", 2)[0].strip()
            err_msg = message_registry.TYPE_COMMENT_SYNTAX_ERROR_VALUE.format(stripped_type)
            errors.report(line, column, err_msg.value, blocker=True, code=err_msg.code)
            return None, None
        else:
            raise
    else:
        extra_ignore = TYPE_IGNORE_PATTERN.match(type_comment)
        if extra_ignore:
            tag: str | None = extra_ignore.group(1)
            ignored: list[str] | None = parse_type_ignore_tag(tag)
            if ignored is None:
                if errors is not None:
                    errors.report(
                        line, column, message_registry.INVALID_TYPE_IGNORE.value, code=codes.SYNTAX
                    )
                else:
                    raise SyntaxError
        else:
            ignored = None
        assert isinstance(typ, ast3.Expression)
        converted = TypeConverter(
            errors, line=line, override_column=column, is_evaluated=False
        ).visit(typ.body)
        return ignored, converted

