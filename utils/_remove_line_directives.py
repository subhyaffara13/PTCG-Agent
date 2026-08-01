
def _remove_line_directives(csource):
    # _r_line_directive matches whole lines, without the final \n, if they
    # start with '#line' with some spacing allowed, or '#NUMBER'.  This
    # function stores them away and replaces them with exactly the string
    # '#line@N', where N is the index in the list 'line_directives'.
    line_directives = []
    def replace(m):
        i = len(line_directives)
        line_directives.append(m.group())
        return '#line@%d' % i
    csource = _r_line_directive.sub(replace, csource)
    return csource, line_directives

