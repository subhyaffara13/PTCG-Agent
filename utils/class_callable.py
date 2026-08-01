
def class_callable(
    init_type: CallableType,
    info: TypeInfo,
    def_info: TypeInfo | None,
    type_type: Instance,
    special_sig: str | None,
    is_new: bool,
    orig_self_type: Type | None = None,
) -> CallableType:
    """Create a type object type based on the signature of __init__."""
    variables: list[TypeVarLikeType] = []
    variables.extend(info.defn.type_vars)
    variables.extend(init_type.variables)

    from mypy.subtypes import is_equivalent, is_subtype

    init_ret_type = get_proper_type(init_type.ret_type)
    orig_self_type = get_proper_type(orig_self_type)
    default_ret_type = fill_typevars(info)
    # Default return type in the class where constructor method was defined.
    default_def_ret_type = fill_typevars(def_info) if def_info is not None else default_ret_type
    explicit_type = init_ret_type if is_new else orig_self_type
    if (
        is_new
        and explicit_type is not None
        # We used to only use the explicit return type of __new__() when it was a subtype
        # of the current class. As a result, we may now have a situation like this:
        #     class C:
        #         def __new__(cls) -> C: ...
        #     class D(C): ...
        # So we need to ignore the explicit annotation when creating constructor type for D.
        and (
            isinstance(explicit_type, AnyType)
            and explicit_type.type_of_any != TypeOfAny.unannotated
            or not is_equivalent(default_def_ret_type, explicit_type, ignore_type_params=True)
        )
    ):
        ret_type = explicit_type
    elif (
        isinstance(explicit_type, (Instance, TupleType, UninhabitedType, LiteralType))
        # We have to skip protocols, because it can be a subtype of a return type
        # by accident. Like `Hashable` is a subtype of `object`. See #11799
        and isinstance(default_ret_type, Instance)
        and not default_ret_type.type.is_protocol
        # Use the declared self in __init__ if it is a subtype of what we would use otherwise.
        and is_subtype(explicit_type, default_ret_type, ignore_type_params=True)
    ):
        ret_type = explicit_type
    else:
        ret_type = default_ret_type

    return init_type.copy_modified(
        ret_type=ret_type,
        fallback=type_type,
        name=info.name,
        variables=variables,
        special_sig=special_sig,
        instance_type=default_ret_type,
    )

