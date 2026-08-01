
def cell_ends_with_function_or_class(lines):
    """Does the last line of the cell belong to an indented code?"""
    non_quoted_lines = []
    parser = StringParser("python")
    for line in lines:
        if not parser.is_quoted():
            non_quoted_lines.append(line)
        parser.read_line(line)

    # find the first line, starting from the bottom, that is not indented
    lines = non_quoted_lines[::-1]
    for i, line in enumerate(lines):
        if not line.strip():
            # two blank lines? we won't need to insert more blank lines below this cell
            if i > 0 and not lines[i - 1].strip():
                return False
            continue
        if line.startswith(("#", " ", ")")):
            continue
        if line.startswith("def ") or line.startswith("async ") or line.startswith("class "):
            return True
        return False

    return False

