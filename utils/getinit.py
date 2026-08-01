
def getinit(a, var):
    if isstring(var):
        init, showinit = '""', "''"
    else:
        init, showinit = '', ''
    if hasinitvalue(var):
        init = var['=']
        showinit = init
        if iscomplex(var) or iscomplexarray(var):
            ret = {}

            try:
                v = var["="]
                if ',' in v:
                    ret['init.r'], ret['init.i'] = markoutercomma(
                        v[1:-1]).split('@,@')
                else:
                    v = eval(v, {}, {})
                    ret['init.r'], ret['init.i'] = str(v.real), str(v.imag)
            except Exception:
                raise ValueError(
                    f'getinit: expected complex number `(r,i)\' but got `{init}\' as initial value of {a!r}.')
            if isarray(var):
                init = f"(capi_c.r={ret['init.r']},capi_c.i={ret['init.i']},capi_c)"
        elif isstring(var):
            if not init:
                init, showinit = '""', "''"
            if init[0] == "'":
                escaped_init = init[1:-1].replace('"', '\\"')
                init = f'"{escaped_init}"'
            if init[0] == '"':
                showinit = f"'{init[1:-1]}'"
    return init, showinit

