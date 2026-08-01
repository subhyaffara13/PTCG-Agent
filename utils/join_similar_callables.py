
def join_similar_callables(t: CallableType, s: CallableType) -> CallableType:
    t, s = match_generic_callables(t, s)
    arg_types: list[Type] = []
    for i in range(len(t.arg_types)):
        arg_types.append(safe_meet(t.arg_types[i], s.arg_types[i]))
    # TODO in combine_similar_callables also applies here (names and kinds; user metaclasses)
    # The fallback type can be either 'function', 'type', or some user-provided metaclass.
    # The result should always use 'function' as a fallback if either operands are using it.
    if t.fallback.type.fullname == "builtins.function":
        fallback = t.fallback
    else:
        fallback = s.fallback
    instance_type = None
    if t.instance_type is not None and s.instance_type is not None:
        instance_type = join_types(t.instance_type, s.instance_type)
    return t.copy_modified(
        arg_types=arg_types,
        arg_names=combine_arg_names(t, s),
        ret_type=join_types(t.ret_type, s.ret_type),
        instance_type=instance_type,
        fallback=fallback,
        name=None,
    )

