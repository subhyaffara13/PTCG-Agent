
def rich_to_html(input_text: str) -> str:
    """Print the HTML version of a rich-formatted input string.

    This function does not provide a full HTML page, but can be used to insert
    HTML-formatted text spans into a markdown file.
    """
    console = Console(record=True, highlight=False, file=io.StringIO())

    console.print(input_text, overflow="ignore", crop=False)

    return console.export_html(inline_styles=True, code_format="{code}").strip()

