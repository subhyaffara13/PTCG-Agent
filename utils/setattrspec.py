
def setattrspec(decl, attr, force=0):
    if not decl:
        decl = {}
    if not attr:
        return decl
    if 'attrspec' not in decl:
        decl['attrspec'] = [attr]
        return decl
    if force:
        decl['attrspec'].append(attr)
    if attr in decl['attrspec']:
        return decl
    if attr == 'static' and 'automatic' not in decl['attrspec']:
        decl['attrspec'].append(attr)
    elif attr == 'automatic' and 'static' not in decl['attrspec']:
        decl['attrspec'].append(attr)
    elif attr == 'public':
        if 'private' not in decl['attrspec']:
            decl['attrspec'].append(attr)
    elif attr == 'private':
        if 'public' not in decl['attrspec']:
            decl['attrspec'].append(attr)
    else:
        decl['attrspec'].append(attr)
    return decl

