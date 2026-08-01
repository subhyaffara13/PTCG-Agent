
def _restore_curry(cls, func, args, kwargs, userdict, is_decorated):
    if isinstance(func, str):
        modname, qualname = func.rsplit(':', 1)
        obj = import_module(modname)
        for attr in qualname.split('.'):
            obj = getattr(obj, attr)
        if is_decorated:
            return obj
        func = obj.func
    obj = cls(func, *args, **(kwargs or {}))
    obj.__dict__.update(userdict)
    return obj

