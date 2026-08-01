
def _module_reduce(obj):
    if _should_pickle_by_reference(obj):
        return subimport, (obj.__name__,)
    else:
        # Some external libraries can populate the "__builtins__" entry of a
        # module's `__dict__` with unpicklable objects (see #316). For that
        # reason, we do not attempt to pickle the "__builtins__" entry, and
        # restore a default value for it at unpickling time.
        state = obj.__dict__.copy()
        state.pop("__builtins__", None)
        return dynamic_subimport, (obj.__name__, state)

