
def get_parameters(vars, global_params={}):
    params = copy.copy(global_params)
    g_params = copy.copy(global_params)
    for name, func in [('kind', _kind_func),
                       ('selected_int_kind', _selected_int_kind_func),
                       ('selected_real_kind', _selected_real_kind_func), ]:
        if name not in g_params:
            g_params[name] = func
    param_names = []
    for n in get_sorted_names(vars):
        if 'attrspec' in vars[n] and 'parameter' in vars[n]['attrspec']:
            param_names.append(n)
    kind_re = re.compile(r'\bkind\s*\(\s*(?P<value>.*)\s*\)', re.I)
    selected_int_kind_re = re.compile(
        r'\bselected_int_kind\s*\(\s*(?P<value>.*)\s*\)', re.I)
    selected_kind_re = re.compile(
        r'\bselected_(int|real)_kind\s*\(\s*(?P<value>.*)\s*\)', re.I)
    for n in param_names:
        if '=' in vars[n]:
            v = vars[n]['=']
            if islogical(vars[n]):
                v = v.lower()
                for repl in [
                    ('.false.', 'False'),
                    ('.true.', 'True'),
                    # TODO: test .eq., .neq., etc replacements.
                ]:
                    v = v.replace(*repl)

            v = kind_re.sub(r'kind("\1")', v)
            v = selected_int_kind_re.sub(r'selected_int_kind(\1)', v)

            # We need to act according to the data.
            # The easy case is if the data has a kind-specifier,
            # then we may easily remove those specifiers.
            # However, it may be that the user uses other specifiers...(!)
            is_replaced = False

            if 'kindselector' in vars[n]:
                # Remove kind specifier (including those defined
                # by parameters)
                if 'kind' in vars[n]['kindselector']:
                    orig_v_len = len(v)
                    v = v.replace('_' + vars[n]['kindselector']['kind'], '')
                    # Again, this will be true if even a single specifier
                    # has been replaced, see comment above.
                    is_replaced = len(v) < orig_v_len

            if not is_replaced:
                if not selected_kind_re.match(v):
                    v_ = v.split('_')
                    # In case there are additive parameters
                    if len(v_) > 1:
                        v = ''.join(v_[:-1]).lower().replace(v_[-1].lower(), '')

            # Currently this will not work for complex numbers.
            # There is missing code for extracting a complex number,
            # which may be defined in either of these:
            #  a) (Re, Im)
            #  b) cmplx(Re, Im)
            #  c) dcmplx(Re, Im)
            #  d) cmplx(Re, Im, <prec>)

            if isdouble(vars[n]):
                tt = list(v)
                for m in real16pattern.finditer(v):
                    tt[m.start():m.end()] = list(
                        v[m.start():m.end()].lower().replace('d', 'e'))
                v = ''.join(tt)

            elif iscomplex(vars[n]):
                outmess(f'get_parameters[TODO]: '
                        f'implement evaluation of complex expression {v}\n')

            dimspec = ([s.removeprefix('dimension').strip()
                        for s in vars[n]['attrspec']
                       if s.startswith('dimension')] or [None])[0]

            # Handle _dp for gh-6624
            # Also fixes gh-20460
            if real16pattern.search(v):
                v = 8
            elif real8pattern.search(v):
                v = 4
            try:
                params[n] = param_eval(v, g_params, params, dimspec=dimspec)
            except Exception as msg:
                params[n] = v
                outmess(f'get_parameters: got "{msg}" on {n!r}\n')

            if isstring(vars[n]) and isinstance(params[n], int):
                params[n] = chr(params[n])
            nl = n.lower()
            if nl != n:
                params[nl] = params[n]
        else:
            print(vars[n])
            outmess(f'get_parameters:parameter {n!r} does not have value?!\n')
    return params

