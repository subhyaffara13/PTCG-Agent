
def _patched_getfile(object):
    if inspect.isclass(object):
        if object.__module__ in _package_imported_modules:
            return _package_imported_modules[object.__module__].__file__
    return _orig_getfile(object)

