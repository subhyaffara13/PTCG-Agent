
def _is_one_liner(logical_line, indent_level, lines, line_number):
    if not STARTSWITH_TOP_LEVEL_REGEX.match(logical_line):
        return False

    line_idx = line_number - 1

    if line_idx < 1:
        prev_indent = 0
    else:
        prev_indent = expand_indent(lines[line_idx - 1])

    if prev_indent > indent_level:
        return False

    while line_idx < len(lines):
        line = lines[line_idx].strip()
        if not line.startswith('@') and STARTSWITH_TOP_LEVEL_REGEX.match(line):
            break
        else:
            line_idx += 1
    else:
        return False  # invalid syntax: EOF while searching for def/class

    next_idx = line_idx + 1
    while next_idx < len(lines):
        if lines[next_idx].strip():
            break
        else:
            next_idx += 1
    else:
        return True  # line is last in the file

    return expand_indent(lines[next_idx]) <= indent_level

