
def _closuredsource(func, alias=''):
    """get source code for closured objects; return a dict of 'name'
    and 'code blocks'"""
    #FIXME: this entire function is a messy messy HACK
    #      - pollutes global namespace
    #      - fails if name of freevars are reused
    #      - can unnecessarily duplicate function code
    from .detect import freevars
    free_vars = freevars(func)
    func_vars = {}
    # split into 'funcs' and 'non-funcs'
    for name,obj in list(free_vars.items()):
        if not isfunction(obj):
            # get source for 'non-funcs'
            free_vars[name] = getsource(obj, force=True, alias=name)
            continue
        # get source for 'funcs'
        fobj = free_vars.pop(name)
        src = getsource(fobj, alias) # DO NOT include dependencies
        # if source doesn't start with '@', use name as the alias
        if not src.lstrip().startswith('@'): #FIXME: 'enclose' in dummy;
            src = importable(fobj,alias=name)#        wrong ref 'name'
            org = getsource(func, alias, enclosing=False, lstrip=True)
            src = (src, org) # undecorated first, then target
        else: #NOTE: reproduces the code!
            org = getsource(func, enclosing=True, lstrip=False)
            src = importable(fobj, alias, source=True) # include dependencies
            src = (org, src) # target first, then decorated
        func_vars[name] = src
    src = ''.join(free_vars.values())
    if not func_vars: #FIXME: 'enclose' in dummy; wrong ref 'name'
        org = getsource(func, alias, force=True, enclosing=False, lstrip=True)
        src = (src, org) # variables first, then target
    else:
        src = (src, None) # just variables        (better '' instead of None?)
    func_vars[None] = src
    # FIXME: remove duplicates (however, order is important...)
    return func_vars

