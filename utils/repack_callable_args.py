
def repack_callable_args(callable: CallableType, tuple_type: TypeInfo) -> list[Type]:
    """Present callable with star unpack in a normalized form.

    Since positional arguments cannot follow star argument, they are packed in a suffix,
    while prefix is represented as individual positional args. We want to put all in a single
    list with unpack in the middle, and prefix/suffix on the sides (as they would appear
    in e.g. a TupleType).
    """
    if ARG_STAR not in callable.arg_kinds:
        return callable.arg_types
    star_index = callable.arg_kinds.index(ARG_STAR)
    arg_types = callable.arg_types[:star_index]
    star_type = callable.arg_types[star_index]
    suffix_types = []
    if not isinstance(star_type, UnpackType):
        # Re-normalize *args: X -> *args: *tuple[X, ...]
        star_type = UnpackType(Instance(tuple_type, [star_type]))
    else:
        tp = get_proper_type(star_type.type)
        if isinstance(tp, TupleType):
            assert isinstance(tp.items[0], UnpackType)
            star_type = tp.items[0]
            suffix_types = tp.items[1:]
    return arg_types + [star_type] + suffix_types

