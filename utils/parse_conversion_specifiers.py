
def parse_conversion_specifiers(format_str: str) -> list[ConversionSpecifier]:
    """Parse c-printf-style format string into list of conversion specifiers."""
    specifiers: list[ConversionSpecifier] = []
    for m in re.finditer(FORMAT_RE, format_str):
        specifiers.append(ConversionSpecifier(m, start_pos=m.start()))
    return specifiers

