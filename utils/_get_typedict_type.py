
def _get_typedict_type(cls, clsdict, attrs, postproc_list):
    """Retrieve a copy of the dict of a class without the inherited methods"""
    if len(cls.__bases__) == 1:
        inherited_dict = cls.__bases__[0].__dict__
    else:
        inherited_dict = {}
        for base in reversed(cls.__bases__):
            inherited_dict.update(base.__dict__)
    to_remove = []
    for name, value in dict.items(clsdict):
        try:
            base_value = inherited_dict[name]
            if value is base_value and hasattr(value, '__qualname__'):
                to_remove.append(name)
        except KeyError:
            pass
    for name in to_remove:
        dict.pop(clsdict, name)

    if issubclass(type(cls), type):
        clsdict.pop('__dict__', None)
        clsdict.pop('__weakref__', None)
        # clsdict.pop('__prepare__', None)
    return clsdict, attrs

