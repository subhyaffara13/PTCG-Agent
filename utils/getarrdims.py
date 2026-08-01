
def getarrdims(a, var, verbose=0):
    ret = {}
    if isstring(var) and not isarray(var):
        ret['size'] = getstrlength(var)
        ret['rank'] = '0'
        ret['dims'] = ''
    elif isscalar(var):
        ret['size'] = '1'
        ret['rank'] = '0'
        ret['dims'] = ''
    elif isarray(var):
        dim = copy.copy(var['dimension'])
        ret['size'] = '*'.join(dim)
        try:
            ret['size'] = repr(eval(ret['size']))
        except Exception:
            pass
        ret['dims'] = ','.join(dim)
        ret['rank'] = repr(len(dim))
        ret['rank*[-1]'] = repr(len(dim) * [-1])[1:-1]
        for i in range(len(dim)):  # solve dim for dependencies
            v = []
            if dim[i] in depargs:
                v = [dim[i]]
            else:
                for va in depargs:
                    if re.match(rf'.*?\b{va}\b.*', dim[i]):
                        v.append(va)
            for va in v:
                if depargs.index(va) > depargs.index(a):
                    dim[i] = '*'
                    break
        ret['setdims'], i = '', -1
        for d in dim:
            i = i + 1
            if d not in ['*', ':', '(*)', '(:)']:
                ret['setdims'] = f"{ret['setdims']}#varname#_Dims[{i}]={d},"
        if ret['setdims']:
            ret['setdims'] = ret['setdims'][:-1]
        ret['cbsetdims'], i = '', -1
        for d in var['dimension']:
            i = i + 1
            if d not in ['*', ':', '(*)', '(:)']:
                ret['cbsetdims'] = f"{ret['cbsetdims']}#varname#_Dims[{i}]={d},"
            elif isintent_in(var):
                outmess('getarrdims:warning: assumed shape array, using 0 '
                        f'instead of {d!r}\n')
                ret['cbsetdims'] = f"{ret['cbsetdims']}#varname#_Dims[{i}]={0},"
            elif verbose:
                errmess(
                    f'getarrdims: If in call-back function: array argument {repr(a)} must have bounded dimensions: got {repr(d)}\n')
        if ret['cbsetdims']:
            ret['cbsetdims'] = ret['cbsetdims'][:-1]
#         if not isintent_c(var):
#             var['dimension'].reverse()
    return ret

