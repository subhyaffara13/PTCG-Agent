
def getctype(var):
    """
    Determines C type
    """
    ctype = 'void'
    if isfunction(var):
        if 'result' in var:
            a = var['result']
        else:
            a = var['name']
        if a in var['vars']:
            return getctype(var['vars'][a])
        else:
            errmess(f'getctype: function {a} has no return value?!\n')
    elif issubroutine(var):
        return ctype
    elif ischaracter_or_characterarray(var):
        return 'character'
    elif isstring_or_stringarray(var):
        return 'string'
    elif 'typespec' in var and var['typespec'].lower() in f2cmap_all:
        typespec = var['typespec'].lower()
        f2cmap = f2cmap_all[typespec]
        ctype = f2cmap['']  # default type
        if 'kindselector' in var:
            if '*' in var['kindselector']:
                try:
                    ctype = f2cmap[var['kindselector']['*']]
                except KeyError:
                    raw_typespec = var['typespec']
                    star = var['kindselector']['*']
                    errmess(f'getctype: "{raw_typespec} * {star}" not supported.\n')
            elif 'kind' in var['kindselector']:
                if typespec + 'kind' in f2cmap_all:
                    f2cmap = f2cmap_all[typespec + 'kind']
                try:
                    ctype = f2cmap[var['kindselector']['kind']]
                except KeyError:
                    if typespec in f2cmap_all:
                        f2cmap = f2cmap_all[typespec]
                    try:
                        ctype = f2cmap[str(var['kindselector']['kind'])]
                    except KeyError:
                        kind = var['kindselector']['kind']
                        errmess(f'getctype: "{typespec}({kind=})" is mapped to C '
                                f'"{ctype}" (to override define {{{typespec!r}: '
                                f'{{{kind!r}: "<C typespec>"}}}} '
                                f'in {os.getcwd()}/.f2py_f2cmap file).\n')
    elif not isexternal(var):
        errmess(f'getctype: No C-type found in "{var}", assuming void.\n')
    return ctype

