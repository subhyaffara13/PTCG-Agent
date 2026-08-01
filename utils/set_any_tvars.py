
def set_any_tvars(
    node: TypeAlias,
    args: list[Type],
    newline: int,
    newcolumn: int,
    options: Options,
    *,
    from_error: bool = False,
    disallow_any: bool = False,
    special_form: bool = False,
    fail: MsgCallback | None = None,
    note: MsgCallback | None = None,
    unexpanded_type: Type | None = None,
    analyzing_tvar_def: bool = False,
) -> tuple[TypeAliasType, bool]:
    used_default = False
    if from_error or disallow_any:
        type_of_any = TypeOfAny.from_error
    elif special_form:
        type_of_any = TypeOfAny.special_form
    else:
        type_of_any = TypeOfAny.from_omitted_generics
    any_type = AnyType(type_of_any, line=newline, column=newcolumn)

    env: dict[TypeVarId, Type] = {}
    used_any_type = False
    for tv, arg in itertools.zip_longest(node.alias_tvars, args, fillvalue=None):
        if tv is None:
            continue
        if arg is None:
            if tv.has_default():
                arg = tv.default
                # Same as for instances, record and avoid infinite recursion.
                if analyzing_tvar_def:
                    used_default = True
                    if is_typevar_default_recursive(tv.fullname, node):
                        arg = any_type
                        used_any_type = True
            else:
                arg = any_type
                used_any_type = True
            if used_any_type and isinstance(tv, TypeVarTupleType):
                arg = UnpackType(Instance(tv.tuple_fallback.type, [any_type]))
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
    t = TypeAliasType(node, args, newline, newcolumn)

    if used_any_type and disallow_any and node.alias_tvars and not from_error:
        assert fail is not None
        if unexpanded_type:
            type_str = (
                unexpanded_type.name
                if isinstance(unexpanded_type, UnboundType)
                else format_type_bare(unexpanded_type, options)
            )
        else:
            type_str = node.name

        fail(
            message_registry.BARE_GENERIC.format(quote_type_string(type_str)),
            Context(newline, newcolumn),
            code=codes.TYPE_ARG,
        )
        if used_default:
            assert note is not None
            note(
                message_registry.NO_CYCLIC_DEFAULT,
                Context(newline, newcolumn),
                code=codes.TYPE_ARG,
            )
    return t, used_default

