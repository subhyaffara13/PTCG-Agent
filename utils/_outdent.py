
def _outdent(lines, spaces=None, all=True):
    '''outdent lines of code, accounting for docs and line continuations'''
    indent = indentsize(lines[0])
    if spaces is None or spaces > indent or spaces < 0: spaces = indent
    for i in range(len(lines) if all else 1):
        #FIXME: works... but shouldn't outdent 2nd+ lines of multiline doc
        _indent = indentsize(lines[i])
        if spaces > _indent: _spaces = _indent
        else: _spaces = spaces
        lines[i] = lines[i][_spaces:]
    return lines

