
def parse_structure(astr):
    """ Return a list of tuples for each function or subroutine each
    tuple is the start and end of a subroutine or function to be
    expanded.
    """

    spanlist = []
    ind = 0
    while True:
        m = routine_start_re.search(astr, ind)
        if m is None:
            break
        start = m.start()
        if function_start_re.match(astr, start, m.end()):
            while True:
                i = astr.rfind('\n', ind, start)
                if i == -1:
                    break
                start = i
                if astr[i:i + 7] != '\n     $':
                    break
        start += 1
        m = routine_end_re.search(astr, m.end())
        ind = end = (m and m.end() - 1) or len(astr)
        spanlist.append((start, end))
    return spanlist

