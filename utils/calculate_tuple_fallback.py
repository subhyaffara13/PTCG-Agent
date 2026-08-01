
def calculate_tuple_fallback(typ: TupleType) -> None:
    """Calculate a precise item type for the fallback of a tuple type.

    This must be called only after the main semantic analysis pass, since joins
    aren't available before that.

    Note that there is an apparent chicken and egg problem with respect
    to verifying type arguments against bounds. Verifying bounds might
    require fallbacks, but we might use the bounds to calculate the
    fallbacks. In practice this is not a problem, since the worst that
    can happen is that we have invalid type argument values, and these
    can happen in later stages as well (they will generate errors, but
    we don't prevent their existence).
    """
    fallback = typ.partial_fallback
    assert fallback.type.fullname == "builtins.tuple"
    items = []
    for item in flatten_nested_tuples(typ.items):
        # TODO: this duplicates some logic in typeops.tuple_fallback().
        if isinstance(item, UnpackType):
            unpacked_type = get_proper_type(item.type)
            if isinstance(unpacked_type, TypeVarTupleType):
                unpacked_type = get_proper_type(unpacked_type.upper_bound)
            if (
                isinstance(unpacked_type, Instance)
                and unpacked_type.type.fullname == "builtins.tuple"
            ):
                items.append(unpacked_type.args[0])
            else:
                # This is called before semanal_typeargs.py fixes broken unpacks,
                # where the error should also be generated.
                items.append(AnyType(TypeOfAny.from_error))
        else:
            items.append(item)
    fallback.args = (make_simplified_union(items),)

