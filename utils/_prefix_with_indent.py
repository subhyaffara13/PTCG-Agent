
def _prefix_with_indent(
    s: Text | str,
    console: Console,
    *,
    prefix: str,
    indent: str,
) -> Text:
    if isinstance(s, Text):
        text = s
    else:
        text = console.render_str(s)

    return console.render_str(prefix, overflow="ignore") + console.render_str(
        f"\n{indent}", overflow="ignore"
    ).join(text.split(allow_blank=True))

