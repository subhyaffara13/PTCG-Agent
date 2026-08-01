
def tabs_obsolete(physical_line):
    r"""On new projects, spaces-only are strongly recommended over tabs.

    Okay: if True:\n    return
    W191: if True:\n\treturn
    """
    indent = INDENT_REGEX.match(physical_line).group(1)
    if '\t' in indent:
        return indent.index('\t'), "W191 indentation contains tabs"

