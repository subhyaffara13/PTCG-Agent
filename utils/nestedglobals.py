
def nestedglobals(func, recurse=True):
    """get the names of any globals found within func"""
    func = code(func)
    if func is None: return list()
    import sys
    from .temp import capture
    CAN_NULL = sys.hexversion >= 0x30b00a7 # NULL may be prepended >= 3.11a7
    names = set()
    with capture('stdout') as out:
        try:
            dis.dis(func) #XXX: dis.dis(None) disassembles last traceback
        except IndexError:
            pass #FIXME: HACK for IS_PYPY (3.11)
    for line in out.getvalue().splitlines():
        if '_GLOBAL' in line:
            name = line.split('(')[-1].split(')')[0]
            if CAN_NULL:
                names.add(name.replace('NULL + ', '').replace(' + NULL', ''))
            else:
                names.add(name)
    for co in getattr(func, 'co_consts', tuple()):
        if co and recurse and iscode(co):
            names.update(nestedglobals(co, recurse=True))
    return list(names)

