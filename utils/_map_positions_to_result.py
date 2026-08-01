
def _map_positions_to_result(
    line: _StrLike,
    search_dict: dict[_StrLike, _BadChar],
    new_line: _StrLike,
    byte_str_length: int = 1,
) -> dict[int, _BadChar]:
    """Get all occurrences of search dict keys within line.

    Ignores Windows end of line and can handle bytes as well as string.
    Also takes care of encodings for which the length of an encoded code point does not
    default to 8 Bit.
    """
    result: dict[int, _BadChar] = {}

    for search_for, char in search_dict.items():
        if search_for not in line:
            continue

        # Special Handling for Windows '\r\n'
        if char.unescaped == "\r" and line.endswith(new_line):
            ignore_pos = len(line) - 2 * byte_str_length
        else:
            ignore_pos = None

        start = 0
        pos = line.find(search_for, start)
        while pos > 0:
            if pos != ignore_pos:
                # Calculate the column
                col = int(pos / byte_str_length)
                result[col] = char
            start = pos + 1
            pos = line.find(search_for, start)

    return result

