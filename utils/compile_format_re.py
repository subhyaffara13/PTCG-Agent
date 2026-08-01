
def compile_format_re() -> Pattern[str]:
    """Construct regexp to match format conversion specifiers in % interpolation.

    See https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting
    The regexp is intentionally a bit wider to report better errors.
    """
    key_re = r"(\((?P<key>[^)]*)\))?"  # (optional) parenthesised sequence of characters.
    flags_re = r"(?P<flags>[#0\-+ ]*)"  # (optional) sequence of flags.
    width_re = r"(?P<width>[1-9][0-9]*|\*)?"  # (optional) minimum field width (* or numbers).
    precision_re = r"(?:\.(?P<precision>\*|[0-9]+)?)?"  # (optional) . followed by * of numbers.
    length_mod_re = r"[hlL]?"  # (optional) length modifier (unused).
    type_re = r"(?P<type>.)?"  # conversion type.
    format_re = "%" + key_re + flags_re + width_re + precision_re + length_mod_re + type_re
    return re.compile(format_re)

