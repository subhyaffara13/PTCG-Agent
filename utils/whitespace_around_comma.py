
def whitespace_around_comma(logical_line):
    r"""Avoid extraneous whitespace after a comma or a colon.

    Note: these checks are disabled by default

    Okay: a = (1, 2)
    E241: a = (1,  2)
    E242: a = (1,\t2)
    """
    line = logical_line
    for m in WHITESPACE_AFTER_COMMA_REGEX.finditer(line):
        found = m.start() + 1
        if '\t' in m.group():
            yield found, "E242 tab after '%s'" % m.group()[0]
        else:
            yield found, "E241 multiple spaces after '%s'" % m.group()[0]

