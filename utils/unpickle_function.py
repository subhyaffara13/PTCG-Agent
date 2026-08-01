
def unpickle_function(mod_name, qname, self_):
    import importlib

    try:
        module = importlib.import_module(mod_name)
        qname = qname.split(".")
        func = module
        for q in qname:
            func = getattr(func, q)

        if self_ is not None:
            func = types.MethodType(func, self_)

        return func
    except (ImportError, AttributeError) as e:
        from pickle import UnpicklingError

        raise UnpicklingError from e

