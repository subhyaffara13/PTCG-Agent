
def rich_abort_error() -> None:
    """Print richly formatted abort error."""
    console = _get_rich_console(stderr=True)
    console.print(ABORTED_TEXT, style=STYLE_ABORTED)

