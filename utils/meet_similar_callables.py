
def meet_similar_callables(t: CallableType, s: CallableType) -> CallableType:
    from mypy.join import match_generic_callables, safe_join

    t, s = match_generic_callables(t, s)
    arg_types: list[Type] = []
    for i in range(len(t.arg_types)):
        arg_types.append(safe_join(t.arg_types[i], s.arg_types[i]))
    # TODO in combine_similar_callables also applies here (names and kinds)
    # The fallback type can be either 'function' or 'type'. The result should have 'function' as
    # fallback only if both operands have it as 'function'.
    if t.fallback.type.fullname != "builtins.function":
        fallback = t.fallback
    else:
        fallback = s.fallback
    if t.instance_type is None:
        instance_type = s.instance_type
    elif s.instance_type is None:
        instance_type = t.instance_type
    else:
        instance_type = meet_types(t.instance_type, s.instance_type)
    return t.copy_modified(
        arg_types=arg_types,
        ret_type=meet_types(t.ret_type, s.ret_type),
        instance_type=instance_type,
        fallback=fallback,
        name=None,
    )

