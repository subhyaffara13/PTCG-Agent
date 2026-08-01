
def soft_wrap(msg: str, max_len: int, first_offset: int, num_indent: int = 0) -> str:
    """Wrap a long error message into few lines.

    Breaks will only happen between words, and never inside a quoted group
    (to avoid breaking types such as "Union[int, str]"). The 'first_offset' is
    the width before the start of first line.

    Pad every next line with 'num_indent' spaces. Every line will be at most 'max_len'
    characters, except if it is a single word or quoted group.

    For example:
               first_offset
        ------------------------
        path/to/file: error: 58: Some very long error message
            that needs to be split in separate lines.
            "Long[Type, Names]" are never split.
        ^^^^--------------------------------------------------
        num_indent           max_len
    """
    words = split_words(msg)
    next_line = words.pop(0)
    lines: list[str] = []
    while words:
        next_word = words.pop(0)
        max_line_len = max_len - num_indent if lines else max_len - first_offset
        # Add 1 to account for space between words.
        if len(next_line) + len(next_word) + 1 <= max_line_len:
            next_line += " " + next_word
        else:
            lines.append(next_line)
            next_line = next_word
    lines.append(next_line)
    padding = "\n" + " " * num_indent
    return padding.join(lines)

