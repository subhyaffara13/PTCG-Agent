
def _make_command_help(
    *,
    help_text: str,
    markup_mode: MarkupModeStrict,
) -> Text | Markdown:
    """Build cli help text for a click group command.

    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).

    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.
    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_RICH and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    return _make_rich_text(
        text=paragraphs[0].strip(),
        style=STYLE_OPTION_HELP,
        markup_mode=markup_mode,
    )

