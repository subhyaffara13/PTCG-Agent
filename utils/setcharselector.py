
def setcharselector(decl, sel, force=0):
    if not decl:
        decl = {}
    if not sel:
        return decl
    if 'charselector' not in decl:
        decl['charselector'] = sel
        return decl

    for k in list(sel.keys()):
        if force or k not in decl['charselector']:
            decl['charselector'][k] = sel[k]
    return decl

