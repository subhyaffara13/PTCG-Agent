
def trailing_blank_lines(physical_line, lines, line_number, total_lines):
    r"""Trailing blank lines are superfluous.

    Okay: spam(1)
    W391: spam(1)\n

    However the last line should end with a new line (warning W292).
    """
    if line_number == total_lines:
        stripped_last_line = physical_line.rstrip('\r\n')
        if physical_line and not stripped_last_line:
            return 0, "W391 blank line at end of file"
        if stripped_last_line == physical_line:
            return len(lines[-1]), "W292 no newline at end of file"

