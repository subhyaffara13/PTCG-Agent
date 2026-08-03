import sys

def _load_backend_lib(backend, name, flags):
    import os
    if not isinstance(name, basestring):
        if sys.platform != "win32" or name is not None:
            return backend.load_library(name, flags)
        name = "c"    # Windows: load_library(None) fails, but this works
                      # on Python 2 (backward compatibility hack only)
    first_error = None
    if '.' in name or '/' in name or os.sep in name:
        try:
            return backend.load_library(name, flags)
        except OSError as e:
            first_error = e
    import ctypes.util
    path = ctypes.util.find_library(name)
    if path is None:
        if name == "c" and sys.platform == "win32" and sys.version_info >= (3,):
            raise OSError("dlopen(None) cannot work on Windows for Python 3 "
                          "(see http://bugs.python.org/issue23606)")
        msg = ("ctypes.util.find_library() did not manage "
               "to locate a library called %r" % (name,))
        if first_error is not None:
            msg = "%s.  Additionally, %s" % (first_error, msg)
        raise OSError(msg)
    return backend.load_library(path, flags)

