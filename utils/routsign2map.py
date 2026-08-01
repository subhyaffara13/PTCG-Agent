
def routsign2map(rout):
    """
    name,NAME,begintitle,endtitle
    rname,ctype,rformat
    routdebugshowvalue
    """
    global lcb_map
    name = rout['name']
    fname = getfortranname(rout)
    ret = {'name': name,
           'texname': name.replace('_', '\\_'),
           'name_lower': name.lower(),
           'NAME': name.upper(),
           'begintitle': gentitle(name),
           'endtitle': gentitle(f'end of {name}'),
           'fortranname': fname,
           'FORTRANNAME': fname.upper(),
           'callstatement': getcallstatement(rout) or '',
           'usercode': getusercode(rout) or '',
           'usercode1': getusercode1(rout) or '',
           }
    if '_' in fname:
        ret['F_FUNC'] = 'F_FUNC_US'
    else:
        ret['F_FUNC'] = 'F_FUNC'
    if '_' in name:
        ret['F_WRAPPEDFUNC'] = 'F_WRAPPEDFUNC_US'
    else:
        ret['F_WRAPPEDFUNC'] = 'F_WRAPPEDFUNC'
    lcb_map = {}
    if 'use' in rout:
        for u in rout['use'].keys():
            if u in cb_rules.cb_map:
                for un in cb_rules.cb_map[u]:
                    ln = un[0]
                    if 'map' in rout['use'][u]:
                        for k in rout['use'][u]['map'].keys():
                            if rout['use'][u]['map'][k] == un[0]:
                                ln = k
                                break
                    lcb_map[ln] = un[1]
    elif rout.get('externals'):
        externals = rout['externals']
        errmess(f"routsign2map: Confused: function {ret['name']} has externals "
                f'{externals!r} but no "use" statement.\n')
    ret['callprotoargument'] = getcallprotoargument(rout, lcb_map) or ''
    if isfunction(rout):
        if 'result' in rout:
            a = rout['result']
        else:
            a = rout['name']
        ret['rname'] = a
        ret['pydocsign'], ret['pydocsignout'] = getpydocsign(a, rout)
        ret['ctype'] = getctype(rout['vars'][a])
        if hasresultnote(rout):
            ret['resultnote'] = rout['vars'][a]['note']
            rout['vars'][a]['note'] = ['See elsewhere.']
        if ret['ctype'] in c2buildvalue_map:
            ret['rformat'] = c2buildvalue_map[ret['ctype']]
        else:
            ret['rformat'] = 'O'
            errmess(f"routsign2map: no c2buildvalue key for type {ret['ctype']!r}\n")
        if debugcapi(rout):
            if ret['ctype'] in cformat_map:
                ret['routdebugshowvalue'] = ("debug-capi:"
                                             f"{a}={cformat_map[ret['ctype']]}")
            if isstringfunction(rout):
                ret['routdebugshowvalue'] = f'debug-capi:slen({a})=%d {a}=\\"%s\\"'
        if isstringfunction(rout):
            ret['rlength'] = getstrlength(rout['vars'][a])
            if ret['rlength'] == '-1':
                errmess("routsign2map: expected explicit specification of the length "
                        "of the string returned by the fortran function "
                        f"{rout['name']!r}; taking 10.\n")
                ret['rlength'] = '10'
    if hasnote(rout):
        ret['note'] = rout['note']
        rout['note'] = ['See elsewhere.']
    return ret

