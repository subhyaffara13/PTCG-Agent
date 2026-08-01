
def _split_by_backtick(s: str) -> list[tuple[bool, str]]:
    """
    Splits a str into substrings along backtick characters (`).

    Disregards backticks inside quotes.

    Parameters
    ----------
    s : str
        The Python source code string.

    Returns
    -------
    substrings: list[tuple[bool, str]]
        List of tuples, where each tuple has two elements:
        The first is a boolean indicating if the substring is backtick-quoted.
        The second is the actual substring.
    """
    substrings = []
    substr: list[str] = []  # Will join into a string before adding to `substrings`
    i = 0
    parse_state = ParseState.DEFAULT
    while i < len(s):
        char = s[i]

        match char:
            case "`":
                # start of a backtick-quoted string
                if parse_state == ParseState.DEFAULT:
                    if substr:
                        substrings.append((False, "".join(substr)))

                    substr = [char]
                    i += 1
                    parse_state = ParseState.IN_BACKTICK
                    continue

                elif parse_state == ParseState.IN_BACKTICK:
                    # escaped backtick inside a backtick-quoted string
                    next_char = s[i + 1] if (i != len(s) - 1) else None
                    if next_char == "`":
                        substr.append(char)
                        substr.append(next_char)
                        i += 2
                        continue

                    # end of the backtick-quoted string
                    else:
                        substr.append(char)
                        substrings.append((True, "".join(substr)))

                        substr = []
                        i += 1
                        parse_state = ParseState.DEFAULT
                        continue
            case "'":
                # start of a single-quoted string
                if parse_state == ParseState.DEFAULT:
                    parse_state = ParseState.IN_SINGLE_QUOTE
                # end of a single-quoted string
                elif (parse_state == ParseState.IN_SINGLE_QUOTE) and (s[i - 1] != "\\"):
                    parse_state = ParseState.DEFAULT
            case '"':
                # start of a double-quoted string
                if parse_state == ParseState.DEFAULT:
                    parse_state = ParseState.IN_DOUBLE_QUOTE
                # end of a double-quoted string
                elif (parse_state == ParseState.IN_DOUBLE_QUOTE) and (s[i - 1] != "\\"):
                    parse_state = ParseState.DEFAULT
        substr.append(char)
        i += 1

    if substr:
        substrings.append((False, "".join(substr)))

    return substrings

