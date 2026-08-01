
def crack2fortrangen(block, tab='\n', as_interface=False):
    global skipfuncs, onlyfuncs

    setmesstext(block)
    ret = ''
    if isinstance(block, list):
        for g in block:
            if g and g['block'] in ['function', 'subroutine']:
                if g['name'] in skipfuncs:
                    continue
                if onlyfuncs and g['name'] not in onlyfuncs:
                    continue
            ret = ret + crack2fortrangen(g, tab, as_interface=as_interface)
        return ret
    prefix = ''
    name = ''
    args = ''
    blocktype = block['block']
    if blocktype == 'program':
        return ''
    argsl = []
    if 'name' in block:
        name = block['name']
    if 'args' in block:
        vars = block['vars']
        for a in block['args']:
            a = expr2name(a, block, argsl)
            if not isintent_callback(vars[a]):
                argsl.append(a)
        if block['block'] == 'function' or argsl:
            args = f"({','.join(argsl)})"
    f2pyenhancements = ''
    if 'f2pyenhancements' in block:
        for k in list(block['f2pyenhancements'].keys()):
            f2pyenhancements = (f"{f2pyenhancements}{tab + tabchar}{k} "
                                f"{block['f2pyenhancements'][k]}")
    intent_lst = block.get('intent', [])[:]
    if blocktype == 'function' and 'callback' in intent_lst:
        intent_lst.remove('callback')
    if intent_lst:
        f2pyenhancements = (f"{f2pyenhancements}{tab + tabchar}"
                            f"intent({','.join(intent_lst)}) {name}")
    use = ''
    if 'use' in block:
        use = use2fortran(block['use'], tab + tabchar)
    common = ''
    if 'common' in block:
        common = common2fortran(block['common'], tab + tabchar)
    if name == 'unknown_interface':
        name = ''
    result = ''
    if 'result' in block:
        result = f" result ({block['result']})"
        if block['result'] not in argsl:
            argsl.append(block['result'])
    body = crack2fortrangen(block['body'], tab + tabchar, as_interface=as_interface)
    vars = vars2fortran(
        block, block['vars'], argsl, tab + tabchar, as_interface=as_interface)
    mess = ''
    if 'from' in block and not as_interface:
        mess = f"! in {block['from']}"
    if 'entry' in block:
        entry_stmts = ''
        for k, i in list(block['entry'].items()):
            entry_stmts = f"{entry_stmts}{tab + tabchar}entry {k}({','.join(i)})"
        body = body + entry_stmts
    if blocktype == 'block data' and name == '_BLOCK_DATA_':
        name = ''
    ret = (f'{tab}{prefix}{blocktype} {name}{args}{result} '
           f'{mess}{f2pyenhancements}{use}{vars}{common}{body}{tab}end '
           f'{blocktype} {name}')
    return ret

