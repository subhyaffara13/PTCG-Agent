
def analyzeargs(block):
    setmesstext(block)
    implicitrules, _ = buildimplicitrules(block)
    if 'args' not in block:
        block['args'] = []
    args = []
    for a in block['args']:
        a = expr2name(a, block, args)
        args.append(a)
    block['args'] = args
    if 'entry' in block:
        for k, args1 in list(block['entry'].items()):
            for a in args1:
                if a not in block['vars']:
                    block['vars'][a] = {}

    for b in block['body']:
        if b['name'] in args:
            if 'externals' not in block:
                block['externals'] = []
            if b['name'] not in block['externals']:
                block['externals'].append(b['name'])
    if 'result' in block and block['result'] not in block['vars']:
        block['vars'][block['result']] = {}
    return block

