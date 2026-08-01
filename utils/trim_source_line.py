
def trim_source_line(line: str, max_len: int, col: int, min_width: int) -> tuple[str, int]:
    """Trim a line of source code to fit into max_len.

    Show 'min_width' characters on each side of 'col' (an error location). If either
    start or end is trimmed, this is indicated by adding '...' there.
    A typical result looks like this:
        ...some_variable = function_to_call(one_arg, other_arg) or...

    Return the trimmed string and the column offset to adjust error location.
    """
    if max_len < 2 * min_width + 1:
        # In case the window is too tiny it is better to still show something.
        max_len = 2 * min_width + 1

    # Trivial case: line already fits in.
    if len(line) <= max_len:
        return line, 0

    # If column is not too large so that there is still min_width after it,
    # the line doesn't need to be trimmed at the start.
    if col + min_width < max_len:
        return line[:max_len] + "...", 0

    # Otherwise, if the column is not too close to the end, trim both sides.
    if col < len(line) - min_width - 1:
        offset = col - max_len + min_width + 1
        return "..." + line[offset : col + min_width + 1] + "...", offset - 3

    # Finally, if the column is near the end, just trim the start.
    return "..." + line[-max_len:], len(line) - max_len - 3

