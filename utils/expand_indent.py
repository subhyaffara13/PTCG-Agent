
def expand_indent(line):
    r"""Return the amount of indentation.

    Tabs are expanded to the next multiple of 8.
    """
    line = line.rstrip('\n\r')
    if '\t' not in line:
        return len(line) - len(line.lstrip())
    result = 0
    for char in line:
        if char == '\t':
            result = result // 8 * 8 + 8
        elif char == ' ':
            result += 1
        else:
            break
    return result


def expand_indent(line: str) -> int:
    r"""Return the amount of indentation.

    Tabs are expanded to the next multiple of 8.

    >>> expand_indent('    ')
    4
    >>> expand_indent('\t')
    8
    >>> expand_indent('       \t')
    8
    >>> expand_indent('        \t')
    16
    """
    return len(line.expandtabs(8))

