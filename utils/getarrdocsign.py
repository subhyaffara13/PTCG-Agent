
def getarrdocsign(a, var):
    ctype = getctype(var)
    if isstring(var) and (not isarray(var)):
        sig = f'{a} : rank-0 array(string(len={getstrlength(var)}),\'c\')'
    elif isscalar(var):
        sig = f'{a} : rank-0 array({c2py_map[ctype]},\'{c2pycode_map[ctype]}\')'
    elif isarray(var):
        dim = var['dimension']
        rank = repr(len(dim))
        dim_str = ','.join(dim)
        sig = (f"{a} : rank-{rank} array('{c2pycode_map[ctype]}') with "
               f"bounds ({dim_str})")
    return sig

