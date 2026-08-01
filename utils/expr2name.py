
def expr2name(a, block, args=[]):
    orig_a = a
    a_is_expr = not analyzeargs_re_1.match(a)
    if a_is_expr:  # `a` is an expression
        implicitrules, attrrules = buildimplicitrules(block)
        at = determineexprtype(a, block['vars'], implicitrules)
        na = 'e_'
        for c in a:
            c = c.lower()
            if c not in string.ascii_lowercase + string.digits:
                c = '_'
            na = na + c
        if na[-1] == '_':
            na = na + 'e'
        else:
            na = na + '_e'
        a = na
        while a in block['vars'] or a in block['args']:
            a = a + 'r'
    if a in args:
        k = 1
        while a + str(k) in args:
            k = k + 1
        a = a + str(k)
    if a_is_expr:
        block['vars'][a] = at
    else:
        if a not in block['vars']:
            block['vars'][a] = block['vars'].get(orig_a, {})
        if 'externals' in block and orig_a in block['externals'] + block['interfaced']:
            block['vars'][a] = setattrspec(block['vars'][a], 'external')
    return a

