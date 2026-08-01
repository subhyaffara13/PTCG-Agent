
def tokenizer_printf_style(format_str: str) -> tuple[list[str], list[FormatOp]] | None:
    """Tokenize a printf-style format string using regex.

    Return:
        A list of string literals and a list of FormatOps.
    """
    literals: list[str] = []
    specifiers: list[ConversionSpecifier] = parse_conversion_specifiers(format_str)
    format_ops = generate_format_ops(specifiers)
    if format_ops is None:
        return None

    last_end = 0
    for spec in specifiers:
        cur_start = spec.start_pos
        literals.append(format_str[last_end:cur_start])
        last_end = cur_start + len(spec.whole_seq)
    literals.append(format_str[last_end:])

    return literals, format_ops

