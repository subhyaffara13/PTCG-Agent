
def cb_sign2map(a, var, index=None):
    ret = {'varname': a}
    ret['varname_i'] = ret['varname']
    ret['ctype'] = getctype(var)
    if ret['ctype'] in c2capi_map:
        ret['atype'] = c2capi_map[ret['ctype']]
        ret['elsize'] = get_elsize(var)
    if ret['ctype'] in cformat_map:
        ret['showvalueformat'] = f"{cformat_map[ret['ctype']]}"
    if isarray(var):
        ret = dictappend(ret, getarrdims(a, var))
    ret['pydocsign'], ret['pydocsignout'] = getpydocsign(a, var)
    if hasnote(var):
        ret['note'] = var['note']
        var['note'] = ['See elsewhere.']
    return ret

