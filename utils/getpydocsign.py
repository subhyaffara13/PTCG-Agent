
def getpydocsign(a, var):
    global lcb_map
    if isfunction(var):
        if 'result' in var:
            af = var['result']
        else:
            af = var['name']
        if af in var['vars']:
            return getpydocsign(af, var['vars'][af])
        else:
            errmess(f'getctype: function {af} has no return value?!\n')
        return '', ''
    sig, sigout = a, a
    opt = ''
    if isintent_in(var):
        opt = 'input'
    elif isintent_inout(var):
        opt = 'in/output'
    out_a = a
    if isintent_out(var):
        for k in var['intent']:
            if k[:4] == 'out=':
                out_a = k[4:]
                break
    init = ''
    ctype = getctype(var)

    if hasinitvalue(var):
        init, showinit = getinit(a, var)
        init = f', optional\\n    Default: {showinit}'
    if isscalar(var):
        if isintent_inout(var):
            sig = (f"{a} : {opt} rank-0 array({c2py_map[ctype]},"
                   f"'{c2pycode_map[ctype]}'){init}")
        else:
            sig = f'{a} : {opt} {c2py_map[ctype]}{init}'
        sigout = f'{out_a} : {c2py_map[ctype]}'
    elif isstring(var):
        if isintent_inout(var):
            sig = (f"{a} : {opt} rank-0 array(string(len={getstrlength(var)}),"
                   f"'c'){init}")
        else:
            sig = f'{a} : {opt} string(len={getstrlength(var)}){init}'
        sigout = f'{out_a} : string(len={getstrlength(var)})'
    elif isarray(var):
        dim = var['dimension']
        rank = repr(len(dim))
        dim_str = ','.join(dim)
        sig = (f"{a} : {opt} rank-{rank} array('{c2pycode_map[ctype]}') with "
               f"bounds ({dim_str}){init}")
        if a == out_a:
            sigout = (f"{a} : rank-{rank} array('{c2pycode_map[ctype]}') with "
                      f"bounds ({dim_str})")
        else:
            sigout = (f"{out_a} : rank-{rank} array('{c2pycode_map[ctype]}') with "
                      f"bounds ({dim_str}) and {a} storage")
    elif isexternal(var):
        ua = ''
        if a in lcb_map and lcb_map[a] in lcb2_map and 'argname' in lcb2_map[lcb_map[a]]:
            ua = lcb2_map[lcb_map[a]]['argname']
            if not ua == a:
                ua = f' => {ua}'
            else:
                ua = ''
        sig = f'{a} : call-back function{ua}'
        sigout = sig
    else:
        errmess(
            f'getpydocsign: Could not resolve docsignature for "{a}".\n')
    return sig, sigout

