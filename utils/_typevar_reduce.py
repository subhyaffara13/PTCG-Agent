
def _typevar_reduce(obj):
    # TypeVar instances require the module information hence why we
    # are not using the _should_pickle_by_reference directly
    module_and_name = _lookup_module_and_qualname(obj, name=obj.__name__)

    if module_and_name is None:
        return (_make_typevar, _decompose_typevar(obj))
    elif _is_registered_pickle_by_value(module_and_name[0]):
        return (_make_typevar, _decompose_typevar(obj))

    return (getattr, module_and_name)

