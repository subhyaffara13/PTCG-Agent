
def does_not_override_dict_iter_methods(user_cls: Any) -> bool:
    return (
        user_cls.items in (dict.items, OrderedDict.items)
        and user_cls.values in (dict.values, OrderedDict.values)
        and user_cls.keys in (dict.keys, OrderedDict.keys)
        and user_cls.__iter__ in (dict.__iter__, OrderedDict.__iter__)
    )

