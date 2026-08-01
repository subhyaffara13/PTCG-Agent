
def applyrules(rules, d, var={}):
    ret = {}
    if isinstance(rules, list):
        for r in rules:
            rr = applyrules(r, d, var)
            ret = dictappend(ret, rr)
            if '_break' in rr:
                break
        return ret
    if '_check' in rules and (not rules['_check'](var)):
        return ret
    if 'need' in rules:
        res = applyrules({'needs': rules['need']}, d, var)
        if 'needs' in res:
            cfuncs.append_needs(res['needs'])

    for k in rules.keys():
        if k == 'separatorsfor':
            ret[k] = rules[k]
            continue
        if isinstance(rules[k], str):
            ret[k] = replace(rules[k], d)
        elif isinstance(rules[k], list):
            ret[k] = []
            for i in rules[k]:
                ar = applyrules({k: i}, d, var)
                if k in ar:
                    ret[k].append(ar[k])
        elif k[0] == '_':
            continue
        elif isinstance(rules[k], dict):
            ret[k] = []
            for k1 in rules[k].keys():
                if isinstance(k1, types.FunctionType) and k1(var):
                    if isinstance(rules[k][k1], list):
                        for i in rules[k][k1]:
                            if isinstance(i, dict):
                                res = applyrules({'supertext': i}, d, var)
                                i = res.get('supertext', '')
                            ret[k].append(replace(i, d))
                    else:
                        i = rules[k][k1]
                        if isinstance(i, dict):
                            res = applyrules({'supertext': i}, d)
                            i = res.get('supertext', '')
                        ret[k].append(replace(i, d))
        else:
            errmess(f'applyrules: ignoring rule {repr(rules[k])}.\n')
        if isinstance(ret[k], list):
            if len(ret[k]) == 1:
                ret[k] = ret[k][0]
            if ret[k] == []:
                del ret[k]
    return ret

