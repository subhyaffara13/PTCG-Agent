
def _locate_function(obj, pickler=None):
    module_name = getattr(obj, '__module__', None)
    if module_name in ['__main__', None] or \
            pickler and is_dill(pickler, child=False) and pickler._session and module_name == pickler._main.__name__:
        return False
    if hasattr(obj, '__qualname__'):
        module = _import_module(module_name, safe=True)
        try:
            found, _ = _getattribute(module, obj.__qualname__)
            return found is obj
        except AttributeError:
            return False
    else:
        found = _import_module(module_name + '.' + obj.__name__, safe=True)
        return found is obj

