
def _closuredimport(func, alias='', builtin=False):
    """get import for closured objects; return a dict of 'name' and 'import'"""
    import re
    from .detect import freevars, outermost
    free_vars = freevars(func)
    func_vars = {}
    # split into 'funcs' and 'non-funcs'
    for name,obj in list(free_vars.items()):
        if not isfunction(obj): continue
        # get import for 'funcs'
        fobj = free_vars.pop(name)
        src = getsource(fobj)
        if src.lstrip().startswith('@'): # we have a decorator
            src = getimport(fobj, alias=alias, builtin=builtin)
        else: # we have to "hack" a bit... and maybe be lucky
            encl = outermost(func)
            # pattern: 'func = enclosing(fobj'
            pat = r'.*[\w\s]=\s*'+getname(encl)+r'\('+getname(fobj)
            mod = getname(getmodule(encl))
            #HACK: get file containing 'outer' function; is func there?
            lines,_ = findsource(encl)
            candidate = [line for line in lines if getname(encl) in line and \
                         re.match(pat, line)]
            if not candidate:
                mod = getname(getmodule(fobj))
                #HACK: get file containing 'inner' function; is func there?
                lines,_ = findsource(fobj)
                candidate = [line for line in lines \
                             if getname(fobj) in line and re.match(pat, line)]
            if not len(candidate): raise TypeError('import could not be found')
            candidate = candidate[-1]
            name = candidate.split('=',1)[0].split()[-1].strip()
            src = _getimport(mod, name, alias=alias, builtin=builtin)
        func_vars[name] = src
    if not func_vars:
        name = outermost(func)
        mod = getname(getmodule(name))
        if not mod or name is func: # then it can be handled by getimport
            name = getname(func, force=True) #XXX: better key?
            src = getimport(func, alias=alias, builtin=builtin)
        else:
            lines,_ = findsource(name)
            # pattern: 'func = enclosing('
            candidate = [line for line in lines if getname(name) in line and \
                         re.match(r'.*[\w\s]=\s*'+getname(name)+r'\(', line)]
            if not len(candidate): raise TypeError('import could not be found')
            candidate = candidate[-1]
            name = candidate.split('=',1)[0].split()[-1].strip()
            src = _getimport(mod, name, alias=alias, builtin=builtin)
        func_vars[name] = src
    return func_vars

