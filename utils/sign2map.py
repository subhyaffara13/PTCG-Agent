import copy

def sign2map(a, var):
    """
    varname,ctype,atype
    init,init.r,init.i,pytype
    vardebuginfo,vardebugshowvalue,varshowvalue
    varrformat

    intent
    """
    out_a = a
    if isintent_out(var):
        for k in var['intent']:
            if k[:4] == 'out=':
                out_a = k[4:]
                break
    ret = {'varname': a, 'outvarname': out_a, 'ctype': getctype(var)}
    intent_flags = []
    for f, s in isintent_dict.items():
        if f(var):
            intent_flags.append(f'F2PY_{s}')
    if intent_flags:
        # TODO: Evaluate intent_flags here.
        ret['intent'] = '|'.join(intent_flags)
    else:
        ret['intent'] = 'F2PY_INTENT_IN'
    if isarray(var):
        ret['varrformat'] = 'N'
    elif ret['ctype'] in c2buildvalue_map:
        ret['varrformat'] = c2buildvalue_map[ret['ctype']]
    else:
        ret['varrformat'] = 'O'
    ret['init'], ret['showinit'] = getinit(a, var)
    if hasinitvalue(var) and iscomplex(var) and not isarray(var):
        ret['init.r'], ret['init.i'] = markoutercomma(
            ret['init'][1:-1]).split('@,@')
    if isexternal(var):
        ret['cbnamekey'] = a
        if a in lcb_map:
            ret['cbname'] = lcb_map[a]
            ret['maxnofargs'] = lcb2_map[lcb_map[a]]['maxnofargs']
            ret['nofoptargs'] = lcb2_map[lcb_map[a]]['nofoptargs']
            ret['cbdocstr'] = lcb2_map[lcb_map[a]]['docstr']
            ret['cblatexdocstr'] = lcb2_map[lcb_map[a]]['latexdocstr']
        else:
            ret['cbname'] = a
            lcb_map_keys = list(lcb_map.keys())
            errmess(f'sign2map: Confused: external {a} is not in '
                    f'lcb_map{lcb_map_keys}.\n')
    if isstring(var):
        ret['length'] = getstrlength(var)
    if isarray(var):
        ret = dictappend(ret, getarrdims(a, var))
        dim = copy.copy(var['dimension'])
    if ret['ctype'] in c2capi_map:
        ret['atype'] = c2capi_map[ret['ctype']]
        ret['elsize'] = get_elsize(var)
    # Debug info
    if debugcapi(var):
        il = [isintent_in, 'input', isintent_out, 'output',
              isintent_inout, 'inoutput', isrequired, 'required',
              isoptional, 'optional', isintent_hide, 'hidden',
              iscomplex, 'complex scalar',
              l_and(isscalar, l_not(iscomplex)), 'scalar',
              isstring, 'string', isarray, 'array',
              iscomplexarray, 'complex array', isstringarray, 'string array',
              iscomplexfunction, 'complex function',
              l_and(isfunction, l_not(iscomplexfunction)), 'function',
              isexternal, 'callback',
              isintent_callback, 'callback',
              isintent_aux, 'auxiliary',
              ]
        rl = []
        for i in range(0, len(il), 2):
            if il[i](var):
                rl.append(il[i + 1])
        if isstring(var):
            rl.append(f"slen({a})={ret['length']}")
        if isarray(var):
            ddim = ','.join(
                map(lambda x, y: f'{x}|{y}', var['dimension'], dim))
            rl.append(f'dims({ddim})')
        rl_str = ','.join(rl)
        if isexternal(var):
            ret['vardebuginfo'] = f"debug-capi:{a}=>{ret['cbname']}:{rl_str}"
        else:
            ret['vardebuginfo'] = (f"debug-capi:{ret['ctype']} "
                                   f"{a}={ret['showinit']}:{rl_str}")
        if isscalar(var):
            if ret['ctype'] in cformat_map:
                ret['vardebugshowvalue'] = f"debug-capi:{a}={cformat_map[ret['ctype']]}"
        if isstring(var):
            ret['vardebugshowvalue'] = f'debug-capi:slen({a})=%d {a}=\\"%s\\"'
        if isexternal(var):
            ret['vardebugshowvalue'] = f'debug-capi:{a}=%p'
    if ret['ctype'] in cformat_map:
        ret['varshowvalue'] = f"#name#:{a}={cformat_map[ret['ctype']]}"
        ret['showvalueformat'] = f"{cformat_map[ret['ctype']]}"
    if isstring(var):
        ret['varshowvalue'] = f'#name#:slen({a})=%d {a}=\\"%s\\"'
    ret['pydocsign'], ret['pydocsignout'] = getpydocsign(a, var)
    if hasnote(var):
        ret['note'] = var['note']
    return ret

