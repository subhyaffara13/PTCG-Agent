
def get_class(lookup_view):
    """
    Convert a string version of a class name to the object.

    For example, get_class('sympy.core.Basic') will return
    class Basic located in module sympy.core
    """
    if isinstance(lookup_view, str):
        mod_name, func_name = get_mod_func(lookup_view)
        if func_name != '':
            lookup_view = getattr(
                __import__(mod_name, {}, {}, ['*']), func_name)
            if not callable(lookup_view):
                raise AttributeError(
                    "'%s.%s' is not a callable." % (mod_name, func_name))
    return lookup_view


def get_class(type_: Type[Any]) -> Union[None, bool, Type[Any]]:
    """
    Tries to get the class of a Type[T] annotation. Returns True if Type is used
    without brackets. Otherwise returns None.
    """
    if type_ is type:
        return True

    if get_origin(type_) is None:
        return None

    args = get_args(type_)
    if not args or not isinstance(args[0], type):
        return True
    else:
        return args[0]

