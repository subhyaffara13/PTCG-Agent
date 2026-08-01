
def parse_ini_data(
    path: str,
    data: str,
    *,
    strip_inline_comments: bool,
    strip_section_whitespace: bool = False,
) -> tuple[Mapping[str, Mapping[str, str]], Mapping[tuple[str, str | None], int]]:
    """Parse INI data and return sections and sources mappings.

    Args:
        path: Path for error messages
        data: INI content as string
        strip_inline_comments: Whether to strip inline comments from values
        strip_section_whitespace: Whether to strip whitespace from section and key names
            (default: False). When True, addresses issue #4 by stripping Unicode whitespace.

    Returns:
        Tuple of (sections_data, sources) where:
        - sections_data: mapping of section -> {name -> value}
        - sources: mapping of (section, name) -> line number
    """
    tokens = parse_lines(
        path,
        data.splitlines(True),
        strip_inline_comments=strip_inline_comments,
        strip_section_whitespace=strip_section_whitespace,
    )

    sources: dict[tuple[str, str | None], int] = {}
    sections_data: dict[str, dict[str, str]] = {}

    for lineno, section, name, value in tokens:
        if section is None:
            raise ParseError(path, lineno, "no section header defined")
        sources[section, name] = lineno
        if name is None:
            if section in sections_data:
                raise ParseError(path, lineno, f"duplicate section {section!r}")
            sections_data[section] = {}
        else:
            if name in sections_data[section]:
                raise ParseError(path, lineno, f"duplicate name {name!r}")
            assert value is not None
            sections_data[section][name] = value

    return sections_data, sources

