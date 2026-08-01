
def globalvars(func, recurse=True, builtin=False):
    """get objects defined in global scope that are referred to by func

    return a dict of {name:object}"""
    if ismethod(func): func = func.__func__
    if isfunction(func):
        globs = vars(getmodule(sum)).copy() if builtin else {}
        # get references from within closure
        orig_func, func = func, set()
        for obj in orig_func.__closure__ or {}:
            try:
                cell_contents = obj.cell_contents
            except ValueError: # cell is empty
                pass
            else:
                _vars = globalvars(cell_contents, recurse, builtin) or {}
                func.update(_vars) #XXX: (above) be wary of infinte recursion?
                globs.update(_vars)
        # get globals
        globs.update(orig_func.__globals__ or {})
        # get names of references
        if not recurse:
            func.update(orig_func.__code__.co_names)
        else:
            func.update(nestedglobals(orig_func.__code__))
            # find globals for all entries of func
            for key in func.copy(): #XXX: unnecessary...?
                nested_func = globs.get(key)
                if nested_func is orig_func:
                   #func.remove(key) if key in func else None
                    continue  #XXX: globalvars(func, False)?
                func.update(globalvars(nested_func, True, builtin))
    elif iscode(func):
        globs = vars(getmodule(sum)).copy() if builtin else {}
       #globs.update(globals())
        if not recurse:
            func = func.co_names # get names
        else:
            orig_func = func.co_name # to stop infinite recursion
            func = set(nestedglobals(func))
            # find globals for all entries of func
            for key in func.copy(): #XXX: unnecessary...?
                if key is orig_func:
                   #func.remove(key) if key in func else None
                    continue  #XXX: globalvars(func, False)?
                nested_func = globs.get(key)
                func.update(globalvars(nested_func, True, builtin))
    else:
        return {}
    #NOTE: if name not in __globals__, then we skip it...
    return dict((name,globs[name]) for name in func if name in globs)

