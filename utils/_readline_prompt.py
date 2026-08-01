
def _readline_prompt(func: t.Callable[[str], str], text: str, err: bool) -> str:
    """Call a prompt function, passing the full prompt on non-Windows so
    readline can handle line editing and cursor positioning correctly.

    On Windows the prompt is written separately via :func:`echo` for
    colorama support, with only the last character passed to *func*.
    """
    if WIN:
        # Write the prompt separately so that we get nice coloring
        # through colorama on Windows.
        echo(text[:-1], nl=False, err=err)
        # Echo the last character to stdout to work around an issue
        # where readline causes backspace to clear the whole line.
        return func(text[-1:])
    if err:
        with redirect_stdout(sys.stderr):
            return func(text)
    return func(text)

