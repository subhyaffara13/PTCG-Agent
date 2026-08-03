import itertools

def _function_getstate(func):
    # - Put func's dynamic attributes (stored in func.__dict__) in state. These
    #   attributes will be restored at unpickling time using
    #   f.__dict__.update(state)
    # - Put func's members into slotstate. Such attributes will be restored at
    #   unpickling time by iterating over slotstate and calling setattr(func,
    #   slotname, slotvalue)
    slotstate = {
        # Hack to circumvent non-predictable memoization caused by string interning.
        # See the inline comment in _class_setstate for details.
        "__name__": "".join(func.__name__),
        "__qualname__": "".join(func.__qualname__),
        "__annotations__": func.__annotations__,
        "__kwdefaults__": func.__kwdefaults__,
        "__defaults__": func.__defaults__,
        "__module__": func.__module__,
        "__doc__": func.__doc__,
        "__closure__": func.__closure__,
    }

    f_globals_ref = _extract_code_globals(func.__code__)
    f_globals = {k: func.__globals__[k] for k in f_globals_ref if k in func.__globals__}

    if func.__closure__ is not None:
        closure_values = list(map(_get_cell_contents, func.__closure__))
    else:
        closure_values = ()

    # Extract currently-imported submodules used by func. Storing these modules
    # in a smoke _cloudpickle_subimports attribute of the object's state will
    # trigger the side effect of importing these modules at unpickling time
    # (which is necessary for func to work correctly once depickled)
    slotstate["_cloudpickle_submodules"] = _find_imported_submodules(
        func.__code__, itertools.chain(f_globals.values(), closure_values)
    )
    slotstate["__globals__"] = f_globals

    # Hack to circumvent non-predictable memoization caused by string interning.
    # See the inline comment in _class_setstate for details.
    state = {"".join(k): v for k, v in func.__dict__.items()}
    return state, slotstate

