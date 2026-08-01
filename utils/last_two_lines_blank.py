
def last_two_lines_blank(source):
    """Are the two last lines blank, and not the third last one?"""
    if len(source) < 3:
        return False
    return not _BLANK_LINE.match(source[-3]) and _BLANK_LINE.match(source[-2]) and _BLANK_LINE.match(source[-1])

