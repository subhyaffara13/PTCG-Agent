
def common_sign2map(a, var):  # obsolete
    ret = {'varname': a, 'ctype': getctype(var)}
    if isstringarray(var):
        ret['ctype'] = 'char'
    if ret['ctype'] in c2capi_map:
        ret['atype'] = c2capi_map[ret['ctype']]
        ret['elsize'] = get_elsize(var)
    if ret['ctype'] in cformat_map:
        ret['showvalueformat'] = f"{cformat_map[ret['ctype']]}"
    if isarray(var):
        ret = dictappend(ret, getarrdims(a, var))
    elif isstring(var):
        ret['size'] = getstrlength(var)
        ret['rank'] = '1'
    ret['pydocsign'], ret['pydocsignout'] = getpydocsign(a, var)
    if hasnote(var):
        ret['note'] = var['note']
        var['note'] = ['See elsewhere.']
    # for strings this returns 0-rank but actually is 1-rank
    ret['arrdocstr'] = getarrdocsign(a, var)
    return ret

