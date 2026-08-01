
def setkindselector(decl, sel, force=0):
    if not decl:
        decl = {}
    if not sel:
        return decl
    if 'kindselector' not in decl:
        decl['kindselector'] = sel
        return decl
    for k in list(sel.keys()):
        if force or k not in decl['kindselector']:
            decl['kindselector'][k] = sel[k]
    return decl

