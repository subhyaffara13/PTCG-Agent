
def nestedcode(func, recurse=True): #XXX: or return dict of {co_name: co} ?
    """get the code objects for any nested functions (e.g. in a closure)"""
    func = code(func)
    if not iscode(func): return [] #XXX: or raise? no matches
    nested = set()
    for co in func.co_consts:
        if co is None: continue
        co = code(co)
        if co:
            nested.add(co)
            if recurse: nested |= set(nestedcode(co, recurse=True))
    return list(nested)

