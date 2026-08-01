
def skip_line(
    line: str,
    in_quote: str,
    index: int,
    section_comments: tuple[str, ...],
    needs_import: bool = True,
) -> tuple[bool, str]:
    """Determine if a given line should be skipped.

    Returns back a tuple containing:

    (skip_line: bool,
     in_quote: str,)
    """
    should_skip = bool(in_quote)
    if '"' in line or "'" in line:
        char_index = 0
        while char_index < len(line):
            if line[char_index] == "\\":
                char_index += 1
            elif in_quote:
                if line[char_index : char_index + len(in_quote)] == in_quote:
                    in_quote = ""
            elif line[char_index] in ("'", '"'):
                long_quote = line[char_index : char_index + 3]
                if long_quote in ('"""', "'''"):
                    in_quote = long_quote
                    char_index += 2
                else:
                    in_quote = line[char_index]
            elif line[char_index] == "#":
                break
            char_index += 1

    if ";" in line.split("#")[0] and needs_import:
        for part in (part.strip() for part in line.split(";")):
            if (
                part
                and not part.startswith("from ")
                and not part.startswith(("import ", "cimport "))
            ):
                should_skip = True

    return (bool(should_skip or in_quote), in_quote)

