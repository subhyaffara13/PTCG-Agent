
def _get_help_text(
    *,
    obj: click.Command | click.Group,
    markup_mode: MarkupModeStrict,
) -> Iterable[Markdown | Text]:
    """Build primary help text for a click command or group.

    Returns the prose help text for a command or group, rendered either as a
    Rich Text object or as Markdown.
    If the command is marked as deprecated, the deprecated string will be prepended.
    """
    # Prepend deprecated status
    if obj.deprecated:
        yield Text(DEPRECATED_STRING, style=STYLE_DEPRECATED)

    # Fetch and dedent the help text
    help_text = inspect.cleandoc(obj.help or "")

    # Trim off anything that comes after \f on its own line
    help_text = help_text.partition("\f")[0]

    # Get the first paragraph
    first_line, *remaining_paragraphs = help_text.split("\n\n")

    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_MARKDOWN and not first_line.startswith("\b"):
        first_line = first_line.replace("\n", " ")
    yield _make_rich_text(
        text=first_line.strip(),
        style=STYLE_HELPTEXT_FIRST_LINE,
        markup_mode=markup_mode,
    )

    # Get remaining lines, remove single line breaks and format as dim
    if remaining_paragraphs:
        # Add a newline inbetween the header and the remaining paragraphs
        yield Text("")
        # Join with double linebreaks for markdown and Rich markup
        remaining_lines = "\n\n".join(remaining_paragraphs)

        yield _make_rich_text(
            text=remaining_lines,
            style=STYLE_HELPTEXT,
            markup_mode=markup_mode,
        )

