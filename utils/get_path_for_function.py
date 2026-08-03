import sys

def get_path_for_function(f):
    """Get the path of the file where the function is defined.

    :returns: the path, or None if one could not be found or f is not a real
        function
    """

    if hasattr(f, "__module__"):
        module_name = f.__module__
    elif hasattr(f, "im_func"):
        module_name = f.im_func.__module__
    else:
        LOG.warning("Cannot resolve file where %s is defined", f)
        return None

    module = sys.modules[module_name]
    if hasattr(module, "__file__"):
        return module.__file__
    else:
        LOG.warning("Cannot resolve file path for module %s", module_name)
        return None

