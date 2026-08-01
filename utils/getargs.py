
def getargs(rout):
    sortargs, args = [], []
    if 'args' in rout:
        args = rout['args']
        if 'sortvars' in rout:
            for a in rout['sortvars']:
                if a in args:
                    sortargs.append(a)
            for a in args:
                if a not in sortargs:
                    sortargs.append(a)
        else:
            sortargs = rout['args']
    return args, sortargs


def getargs(co):
    """Get information about the arguments accepted by a code object.

    Three things are returned: (args, varargs, varkw), where 'args' is
    a list of argument names (possibly containing nested lists), and
    'varargs' and 'varkw' are the names of the * and ** arguments or None.

    """

    if not iscode(co):
        raise TypeError('arg is not a code object')

    nargs = co.co_argcount
    names = co.co_varnames
    args = list(names[:nargs])

    # The following acrobatics are for anonymous (tuple) arguments.
    # Which we do not need to support, so remove to avoid importing
    # the dis module.
    for i in range(nargs):
        if args[i][:1] in ['', '.']:
            raise TypeError("tuple function arguments are not supported")
    varargs = None
    if co.co_flags & CO_VARARGS:
        varargs = co.co_varnames[nargs]
        nargs = nargs + 1
    varkw = None
    if co.co_flags & CO_VARKEYWORDS:
        varkw = co.co_varnames[nargs]
    return args, varargs, varkw

