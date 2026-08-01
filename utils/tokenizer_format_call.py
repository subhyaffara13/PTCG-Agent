
def tokenizer_format_call(format_str: str) -> tuple[list[str], list[FormatOp]] | None:
    """Tokenize a str.format() format string.

    The core function parse_format_value() is shared with mypy.
    With these specifiers, we then parse the literal substrings
    of the original format string and convert `ConversionSpecifier`
    to `FormatOp`.

    Return:
        A list of string literals and a list of FormatOps. The literals
        are interleaved with FormatOps and the length of returned literals
        should be exactly one more than FormatOps.
        Return None if it cannot parse the string.
    """
    # Creates an empty MessageBuilder here.
    # It wouldn't be used since the code has passed the type-checking.
    specifiers = parse_format_value(
        format_str, EMPTY_CONTEXT, MessageBuilder(Errors(Options()), {})
    )
    if specifiers is None:
        return None
    format_ops = generate_format_ops(specifiers)
    if format_ops is None:
        return None

    literals: list[str] = []
    last_end = 0
    for spec in specifiers:
        # Skip { and }
        literals.append(format_str[last_end : spec.start_pos - 1])
        last_end = spec.start_pos + len(spec.whole_seq) + 1
    literals.append(format_str[last_end:])
    # Deal with escaped {{
    literals = [x.replace("{{", "{").replace("}}", "}") for x in literals]

    return literals, format_ops

