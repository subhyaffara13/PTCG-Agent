
def is_inherently_out_of_scope(obj):
    # modules, exceptions, and things that are not named callables
    # are inherently out of scope.
    return (
        isinstance(obj, ModuleType)
        or (isinstance(obj, type) and issubclass(obj, Exception))
        or not (callable(obj) and hasattr(obj, "__name__"))
    )

