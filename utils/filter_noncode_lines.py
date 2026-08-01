
def filter_noncode_lines(
    ls_1: LineSet,
    stindex_1: Index,
    ls_2: LineSet,
    stindex_2: Index,
    common_lines_nb: int,
) -> int:
    """Return the effective number of common lines between lineset1
    and lineset2 filtered from non code lines.

    That is to say the number of common successive stripped
    lines except those that do not contain code (for example
    a line with only an ending parenthesis)

    :param ls_1: first lineset
    :param stindex_1: first lineset starting index
    :param ls_2: second lineset
    :param stindex_2: second lineset starting index
    :param common_lines_nb: number of common successive stripped lines before being filtered from non code lines
    :return: the number of common successive stripped lines that contain code
    """
    stripped_l1 = [
        lspecif.text
        for lspecif in ls_1.stripped_lines[stindex_1 : stindex_1 + common_lines_nb]
        if REGEX_FOR_LINES_WITH_CONTENT.match(lspecif.text)
    ]
    stripped_l2 = [
        lspecif.text
        for lspecif in ls_2.stripped_lines[stindex_2 : stindex_2 + common_lines_nb]
        if REGEX_FOR_LINES_WITH_CONTENT.match(lspecif.text)
    ]
    return sum(sline_1 == sline_2 for sline_1, sline_2 in zip(stripped_l1, stripped_l2))

