
def vars2fortran(block, vars, args, tab='', as_interface=False):
    setmesstext(block)
    ret = ''
    nout = []
    for a in args:
        if a in block['vars']:
            nout.append(a)
    if 'commonvars' in block:
        for a in block['commonvars']:
            if a in vars:
                if a not in nout:
                    nout.append(a)
            else:
                errmess(
                    f'vars2fortran: Confused?!: "{a}" is not defined in vars.\n')
    if 'varnames' in block:
        nout.extend(block['varnames'])
    if not as_interface:
        for a in list(vars.keys()):
            if a not in nout:
                nout.append(a)
    for a in nout:
        if 'depend' in vars[a]:
            for d in vars[a]['depend']:
                if d in vars and 'depend' in vars[d] and a in vars[d]['depend']:
                    errmess(
                        f'vars2fortran: Warning: cross-dependence between variables "{a}" and "{d}\"\n')
        if 'externals' in block and a in block['externals']:
            if isintent_callback(vars[a]):
                ret = f'{ret}{tab}intent(callback) {a}'
            ret = f'{ret}{tab}external {a}'
            if isoptional(vars[a]):
                ret = f'{ret}{tab}optional {a}'
            if a in vars and 'typespec' not in vars[a]:
                continue
            cont = 1
            for b in block['body']:
                if a == b['name'] and b['block'] == 'function':
                    cont = 0
                    break
            if cont:
                continue
        if a not in vars:
            show(vars)
            outmess(f'vars2fortran: No definition for argument "{a}".\n')
            continue
        if a == block['name']:
            if block['block'] != 'function' or block.get('result'):
                # 1) skip declaring a variable that name matches with
                #    subroutine name
                # 2) skip declaring function when its type is
                #    declared via `result` construction
                continue
        if 'typespec' not in vars[a]:
            if 'attrspec' in vars[a] and 'external' in vars[a]['attrspec']:
                if a in args:
                    ret = f'{ret}{tab}external {a}'
                continue
            show(vars[a])
            outmess(f'vars2fortran: No typespec for argument "{a}".\n')
            continue
        vardef = vars[a]['typespec']
        if vardef == 'type' and 'typename' in vars[a]:
            vardef = f"{vardef}({vars[a]['typename']})"
        selector = {}
        if 'kindselector' in vars[a]:
            selector = vars[a]['kindselector']
        elif 'charselector' in vars[a]:
            selector = vars[a]['charselector']
        if '*' in selector:
            if selector['*'] in ['*', ':']:
                vardef = f"{vardef}*({selector['*']})"
            else:
                vardef = f"{vardef}*{selector['*']}"
        elif 'len' in selector:
            vardef = f"{vardef}(len={selector['len']}"
            if 'kind' in selector:
                vardef = f"{vardef},kind={selector['kind']})"
            else:
                vardef = f'{vardef})'
        elif 'kind' in selector:
            vardef = f"{vardef}(kind={selector['kind']})"
        c = ' '
        if 'attrspec' in vars[a]:
            attr = [l for l in vars[a]['attrspec']
                    if l not in ['external']]
            if as_interface and 'intent(in)' in attr and 'intent(out)' in attr:
                # In Fortran, intent(in, out) are conflicting while
                # intent(in, out) can be specified only via
                # `!f2py intent(out) ..`.
                # So, for the Fortran interface, we'll drop
                # intent(out) to resolve the conflict.
                attr.remove('intent(out)')
            if attr:
                vardef = f"{vardef}, {','.join(attr)}"
                c = ','
        if 'dimension' in vars[a]:
            vardef = f"{vardef}{c}dimension({','.join(vars[a]['dimension'])})"
            c = ','
        if 'intent' in vars[a]:
            lst = true_intent_list(vars[a])
            if lst:
                vardef = f"{vardef}{c}intent({','.join(lst)})"
            c = ','
        if 'check' in vars[a]:
            vardef = f"{vardef}{c}check({','.join(vars[a]['check'])})"
            c = ','
        if 'depend' in vars[a]:
            vardef = f"{vardef}{c}depend({','.join(vars[a]['depend'])})"
            c = ','
        if '=' in vars[a]:
            v = vars[a]['=']
            if vars[a]['typespec'] in ['complex', 'double complex']:
                try:
                    v = eval(v)
                    v = f'({v.real},{v.imag})'
                except Exception:
                    pass
            vardef = f'{vardef} :: {a}={v}'
        else:
            vardef = f'{vardef} :: {a}'
        ret = f'{ret}{tab}{vardef}'
    return ret

