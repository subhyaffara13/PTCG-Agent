
def use2fortran(use, tab=''):
    ret = ''
    for m in list(use.keys()):
        ret = f'{ret}{tab}use {m},'
        if use[m] == {}:
            if ret and ret[-1] == ',':
                ret = ret[:-1]
            continue
        if 'only' in use[m] and use[m]['only']:
            ret = f'{ret} only:'
        if 'map' in use[m] and use[m]['map']:
            c = ' '
            for k in list(use[m]['map'].keys()):
                if k == use[m]['map'][k]:
                    ret = f'{ret}{c}{k}'
                    c = ','
                else:
                    ret = f"{ret}{c}{k}=>{use[m]['map'][k]}"
                    c = ','
        if ret and ret[-1] == ',':
            ret = ret[:-1]
    return ret

