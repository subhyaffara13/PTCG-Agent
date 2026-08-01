
def appenddecl(decl, decl2, force=1):
    if not decl:
        decl = {}
    if not decl2:
        return decl
    if decl is decl2:
        return decl
    for k in list(decl2.keys()):
        if k == 'typespec':
            if force or k not in decl:
                decl[k] = decl2[k]
        elif k == 'attrspec':
            for l in decl2[k]:
                decl = setattrspec(decl, l, force)
        elif k == 'kindselector':
            decl = setkindselector(decl, decl2[k], force)
        elif k == 'charselector':
            decl = setcharselector(decl, decl2[k], force)
        elif k in ['=', 'typename']:
            if force or k not in decl:
                decl[k] = decl2[k]
        elif k == 'note':
            pass
        elif k in ['intent', 'check', 'dimension', 'optional',
                   'required', 'depend']:
            errmess(f'appenddecl: "{k}" not implemented.\n')
        else:
            raise Exception('appenddecl: Unknown variable definition key: ' +
                            str(k))
    return decl

