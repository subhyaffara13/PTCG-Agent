
def convert_type(ty: None, default: None = None) -> StringParamType: ...


def convert_type(
    ty: type | ParamType[t.Any], default: t.Any | None = None
) -> ParamType[t.Any]: ...


def convert_type(
    ty: t.Any | None, default: t.Any | None = None
) -> ParamType[t.Any]: ...


def convert_type(
    ty: t.Any | None = None, default: t.Any | None = None
) -> ParamType[t.Any]:
    """Find the most appropriate :class:`ParamType` for the given Python
    type. If the type isn't provided, it can be inferred from a default
    value.
    """
    guessed = _guess_type(ty, default)
    is_guessed = guessed is not ty

    if isinstance(guessed, tuple):
        return Tuple(guessed)

    if isinstance(guessed, ParamType):
        return guessed

    if guessed is str or guessed is None:
        return STRING

    if guessed is int:
        return INT

    if guessed is float:
        return FLOAT

    if guessed is bool:
        return BOOL

    if is_guessed:
        return STRING

    if __debug__:
        try:
            if issubclass(guessed, ParamType):
                raise AssertionError(
                    f"Attempted to use an uninstantiated parameter type ({guessed})."
                )
        except TypeError:
            # guessed is an instance (correct), so issubclass fails.
            pass

    return FuncParamType(guessed)


def convert_type(typ: Type) -> Json:
    if type(typ) is TypeAliasType:
        return convert_type_alias_type(typ)
    typ = get_proper_type(typ)
    if isinstance(typ, Instance):
        return convert_instance(typ)
    elif isinstance(typ, AnyType):
        return convert_any_type(typ)
    elif isinstance(typ, NoneType):
        return convert_none_type(typ)
    elif isinstance(typ, UnionType):
        return convert_union_type(typ)
    elif isinstance(typ, TupleType):
        return convert_tuple_type(typ)
    elif isinstance(typ, CallableType):
        return convert_callable_type(typ)
    elif isinstance(typ, Overloaded):
        return convert_overloaded(typ)
    elif isinstance(typ, LiteralType):
        return convert_literal_type(typ)
    elif isinstance(typ, TypeVarType):
        return convert_type_var_type(typ)
    elif isinstance(typ, TypeType):
        return convert_type_type(typ)
    elif isinstance(typ, UninhabitedType):
        return convert_uninhabited_type(typ)
    elif isinstance(typ, UnpackType):
        return convert_unpack_type(typ)
    elif isinstance(typ, ParamSpecType):
        return convert_param_spec_type(typ)
    elif isinstance(typ, TypeVarTupleType):
        return convert_type_var_tuple_type(typ)
    elif isinstance(typ, Parameters):
        return convert_parameters(typ)
    elif isinstance(typ, TypedDictType):
        return convert_typeddict_type(typ)
    elif isinstance(typ, UnboundType):
        return convert_unbound_type(typ)
    return {"ERROR": f"{type(typ)!r} unrecognized"}


def convert_type(x, xp):
    # Convert NumPy array to xp-array
    # Convert string to indicated dtype from xp
    # Return Python scalars unchanged
    if isinstance(x, np.ndarray):
        return xp.asarray(x)
    elif isinstance(x, str):
        return getattr(xp, x)
    return x

