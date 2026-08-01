
def _parse_latex_options_strip(value: str | float, arg: str) -> str:
    """
    Strip a css_value which may have latex wrapping arguments, css comment identifiers,
    and whitespaces, to a valid string for latex options parsing.

    For example: 'red /* --wrap */  ' --> 'red'
    """
    return str(value).replace(arg, "").replace("/*", "").replace("*/", "").strip()

