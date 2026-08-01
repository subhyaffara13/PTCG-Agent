
def fix_instance(
    t: Instance,
    fail: MsgCallback,
    note: MsgCallback,
    disallow_any: bool,
    options: Options,
    use_generic_error: bool = False,
    unexpanded_type: Type | None = None,
    analyzing_tvar_def: bool = False,
) -> bool:
    """Fix a malformed instance by replacing all type arguments with TypeVar default or Any.

    Also emit a suitable error if this is not due to implicit Any's.
    """
    used_default = False
    arg_count = len(t.args)
    min_tv_count = sum(
        not tv.has_default() and not isinstance(tv, TypeVarTupleType)
        for tv in t.type.defn.type_vars
    )
    max_tv_count = len(t.type.type_vars)
    if arg_count < min_tv_count or arg_count > max_tv_count:
        # Don't use existing args if arg_count doesn't match
        if arg_count > max_tv_count:
            # Already wrong arg count error, don't emit missing type parameters error as well.
            disallow_any = False
        t.args = ()

    args: list[Type] = list(t.args)
    any_type: AnyType | None = None
    env: dict[TypeVarId, Type] = {}
    tvt_no_default = False

    for tv, arg in itertools.zip_longest(t.type.defn.type_vars, t.args, fillvalue=None):
        if tv is None:
            continue
        if arg is None:
            use_any = False
            if tv.has_default():
                arg = tv.default
                if analyzing_tvar_def:
                    # Record the use of default only when analyzing another default.
                    used_default = True
                    if is_typevar_default_recursive(tv.fullname, t.type):
                        # If this results in infinite recursion, use Any instead.
                        use_any = True
            else:
                use_any = True
            if use_any:
                if any_type is None:
                    fullname = None if use_generic_error else t.type.fullname
                    any_type = get_omitted_any(
                        disallow_any,
                        fail,
                        note,
                        t,
                        options,
                        fullname,
                        unexpanded_type,
                        used_default,
                    )
                arg = any_type
            else:
                assert arg is not None
            if use_any and isinstance(tv, TypeVarTupleType):
                tvt_no_default = True
            # Default such as *tuple[int, str] should be unpacked into individual items.
            if isinstance(arg, UnpackType) and isinstance(
                unpack := get_proper_type(arg.type), TupleType
            ):
                unpacked = unpack.items
            else:
                unpacked = [arg]
            for arg in unpacked:
                with state.strict_optional_set(options.strict_optional):
                    # Gradually expand defaults, as they may depend on previous variables.
                    if tv.has_default():
                        arg = expand_type(arg, env)
                    env[tv.id] = arg
                args.append(arg)
        else:
            env[tv.id] = arg
    t.args = tuple(args)
    if tvt_no_default:
        fix_type_var_tuple_argument(t)
    return used_default

