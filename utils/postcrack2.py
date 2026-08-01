
def postcrack2(block, tab='', param_map=None):
    global f90modulevars

    if not f90modulevars:
        return block
    if isinstance(block, list):
        ret = [postcrack2(g, tab=tab + '\t', param_map=param_map)
               for g in block]
        return ret
    setmesstext(block)
    outmess(f"{tab}Block: {block['name']}\n", 0)

    if param_map is None:
        param_map = get_useparameters(block)

    if param_map is not None and 'vars' in block:
        vars = block['vars']
        for n in list(vars.keys()):
            var = vars[n]
            if 'kindselector' in var:
                kind = var['kindselector']
                if 'kind' in kind:
                    val = kind['kind']
                    if val in param_map:
                        kind['kind'] = param_map[val]
    new_body = [postcrack2(b, tab=tab + '\t', param_map=param_map)
                for b in block['body']]
    block['body'] = new_body

    return block

