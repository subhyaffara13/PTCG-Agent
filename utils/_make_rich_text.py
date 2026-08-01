
def _make_rich_text(
    *, text: str, style: str = "", markup_mode: MarkupModeStrict
) -> Markdown | Text:
    """Take a string, remove indentations, and return styled text.

    If `markup_mode` is `"rich"`, the text is parsed for Rich markup strings.
    If `markup_mode` is `"markdown"`, parse as Markdown.
    """
    # Remove indentations from input text
    text = inspect.cleandoc(text)
    if markup_mode == MARKUP_MODE_MARKDOWN:
        text = Emoji.replace(text)
        return Markdown(text, style=style)
    else:
        assert markup_mode == MARKUP_MODE_RICH
        if _has_ansi_character(text):
            return highlighter(Text.from_ansi(text, style=style))
        else:
            return highlighter(Text.from_markup(text, style=style))

