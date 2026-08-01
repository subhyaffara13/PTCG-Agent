
def rfc822_escape(header: str) -> str:
    """Return a version of the string escaped for inclusion in an
    RFC-822 header, by ensuring there are 8 spaces space after each newline.
    """
    indent = 8 * " "
    lines = header.splitlines(keepends=True)

    # Emulate the behaviour of `str.split`
    # (the terminal line break in `splitlines` does not result in an extra line):
    ends_in_newline = lines and lines[-1].splitlines()[0] != lines[-1]
    suffix = indent if ends_in_newline else ""

    return indent.join(lines) + suffix

