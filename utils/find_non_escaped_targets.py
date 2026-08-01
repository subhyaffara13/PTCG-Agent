
def find_non_escaped_targets(
    format_value: str, ctx: Context, msg: MessageBuilder
) -> list[tuple[str, int]] | None:
    """Return list of raw (un-parsed) format specifiers in format string.

    Format specifiers don't include enclosing braces. We don't use regexp for
    this because they don't work well with nested/repeated patterns
    (both greedy and non-greedy), and these are heavily used internally for
    representation of f-strings.

    Return None in case of an error.
    """
    result = []
    next_spec = ""
    pos = 0
    nesting = 0
    while pos < len(format_value):
        c = format_value[pos]
        if not nesting:
            # Skip any paired '{{' and '}}', enter nesting on '{', report error on '}'.
            if c == "{":
                if pos < len(format_value) - 1 and format_value[pos + 1] == "{":
                    pos += 1
                else:
                    nesting = 1
            if c == "}":
                if pos < len(format_value) - 1 and format_value[pos + 1] == "}":
                    pos += 1
                else:
                    msg.fail(
                        "Invalid conversion specifier in format string: unexpected }",
                        ctx,
                        code=codes.STRING_FORMATTING,
                    )
                    return None
        else:
            # Adjust nesting level, then either continue adding chars or move on.
            if c == "{":
                nesting += 1
            if c == "}":
                nesting -= 1
            if nesting:
                next_spec += c
            else:
                result.append((next_spec, pos - len(next_spec)))
                next_spec = ""
        pos += 1
    if nesting:
        msg.fail(
            "Invalid conversion specifier in format string: unmatched {",
            ctx,
            code=codes.STRING_FORMATTING,
        )
        return None
    return result

