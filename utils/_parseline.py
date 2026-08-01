
def _parseline(
    path: str,
    line: str,
    lineno: int,
    strip_inline_comments: bool,
    strip_section_whitespace: bool,
) -> tuple[str | None, str | None]:
    # blank lines
    if iscommentline(line):
        line = ""
    else:
        line = line.rstrip()
    if not line:
        return None, None
    # section
    if line[0] == "[":
        realline = line
        for c in COMMENTCHARS:
            line = line.split(c)[0].rstrip()
        if line[-1] == "]":
            section_name = line[1:-1]
            # Optionally strip whitespace from section name (issue #4)
            if strip_section_whitespace:
                section_name = section_name.strip()
            return section_name, None
        return None, realline.strip()
    # value
    elif not line[0].isspace():
        try:
            name, value = line.split("=", 1)
            if ":" in name:
                raise ValueError()
        except ValueError:
            try:
                name, value = line.split(":", 1)
            except ValueError:
                raise ParseError(path, lineno, f"unexpected line: {line!r}") from None

        # Strip key name (always for backward compatibility, optionally with unicode awareness)
        key_name = name.strip()

        # Strip value
        value = value.strip()
        # Strip inline comments from values if requested (issue #55)
        if strip_inline_comments:
            for c in COMMENTCHARS:
                value = value.split(c)[0].rstrip()

        return key_name, value
    # continuation
    else:
        line = line.strip()
        # Strip inline comments from continuations if requested (issue #55)
        if strip_inline_comments:
            for c in COMMENTCHARS:
                line = line.split(c)[0].rstrip()
        return None, line

