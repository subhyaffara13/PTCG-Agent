
def _isinstance(object):
    '''True if object is a class instance type (and is not a builtin)'''
    if _hascode(object) or isclass(object) or ismodule(object):
        return False
    if istraceback(object) or isframe(object) or iscode(object):
        return False
    # special handling (numpy arrays, ...)
    if not getmodule(object) and getmodule(type(object)).__name__ in ['numpy']:
        return True
#   # check if is instance of a builtin
#   if not getmodule(object) and getmodule(type(object)).__name__ in ['__builtin__','builtins']:
#       return False
    _types = ('<class ',"<type 'instance'>")
    if not repr(type(object)).startswith(_types): #FIXME: weak hack
        return False
    if not getmodule(object) or object.__module__ in ['builtins','__builtin__'] or getname(object, force=True) in ['array']:
        return False
    return True # by process of elimination... it's what we want


def _isinstance(obj, target_type) -> bool:
    if isinstance(target_type, collections.abc.Container):
        if not isinstance(target_type, tuple):
            raise RuntimeError(
                "The second argument to "
                "`torch.jit.isinstance` must be a type "
                "or a tuple of types"
            )
        for t_type in target_type:
            if _isinstance(obj, t_type):
                return True
        return False

    origin_type = get_origin(target_type)
    if origin_type:
        return container_checker(obj, target_type)

    # Check to handle non-typed optional origin returns as none instead
    #    of as optional in 3.7-3.8
    check_args_exist(target_type)

    # handle non-containers
    return isinstance(obj, target_type)

