
def trailing_whitespace(physical_line):
    r"""Trailing whitespace is superfluous.

    The warning returned varies on whether the line itself is blank,
    for easier filtering for those who want to indent their blank lines.

    Okay: spam(1)\n#
    W291: spam(1) \n#
    W293: class Foo(object):\n    \n    bang = 12
    """
    # Strip these trailing characters:
    # - chr(10), newline
    # - chr(13), carriage return
    # - chr(12), form feed, ^L
    physical_line = physical_line.rstrip('\n\r\x0c')
    stripped = physical_line.rstrip(' \t\v')
    if physical_line != stripped:
        if stripped:
            return len(stripped), "W291 trailing whitespace"
        else:
            return 0, "W293 blank line contains whitespace"

