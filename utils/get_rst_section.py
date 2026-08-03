from typing import Any

def get_rst_section(
    section: str | None,
    options: list[tuple[str, OptionDict, Any]],
    doc: str | None = None,
) -> str:
    """Format an option's section using as a ReStructuredText formatted output."""
    result = ""
    if section:
        result += get_rst_title(section, "'")
    if doc:
        formatted_doc = normalize_text(doc)
        result += f"{formatted_doc}\n\n"
    for optname, optdict, value in options:
        help_opt = optdict.get("help")
        result += f":{optname}:\n"
        if help_opt:
            assert isinstance(help_opt, str)
            formatted_help = normalize_text(help_opt, indent="  ")
            result += f"{formatted_help}\n"
        if value and optname != "py-version":
            value = str(_format_option_value(optdict, value))
            result += f"\n  Default: ``{value.replace('`` ', '```` ``')}``\n"
    return result

