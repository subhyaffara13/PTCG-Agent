
def _get_typedict_abc(obj, _dict, attrs, postproc_list):
    if hasattr(abc, '_get_dump'):
        (registry, _, _, _) = abc._get_dump(obj)
        register = obj.register
        postproc_list.extend((register, (reg(),)) for reg in registry)
    elif hasattr(obj, '_abc_registry'):
        registry = obj._abc_registry
        register = obj.register
        postproc_list.extend((register, (reg,)) for reg in registry)
    else:
        raise PicklingError("Cannot find registry of ABC %s", obj)

    if '_abc_registry' in _dict:
        _dict.pop('_abc_registry', None)
        _dict.pop('_abc_cache', None)
        _dict.pop('_abc_negative_cache', None)
        # _dict.pop('_abc_negative_cache_version', None)
    else:
        _dict.pop('_abc_impl', None)
    return _dict, attrs

