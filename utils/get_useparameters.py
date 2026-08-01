
def get_useparameters(block, param_map=None):
    global f90modulevars

    if param_map is None:
        param_map = {}
    usedict = get_usedict(block)
    if not usedict:
        return param_map
    for usename, mapping in list(usedict.items()):
        usename = usename.lower()
        if usename not in f90modulevars:
            outmess(f'get_useparameters: no module {usename} info used by '
                    f'{block.get("name")}\n')
            continue
        mvars = f90modulevars[usename]
        params = get_parameters(mvars)
        if not params:
            continue
        # XXX: apply mapping
        if mapping:
            errmess(f'get_useparameters: mapping for {mapping} not impl.\n')
        for k, v in list(params.items()):
            if k in param_map:
                outmess(f'get_useparameters: overriding parameter {k!r} with'
                        f' value from module {usename!r}\n')
            param_map[k] = v

    return param_map

