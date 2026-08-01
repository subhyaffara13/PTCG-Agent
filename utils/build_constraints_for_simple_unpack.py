
def build_constraints_for_simple_unpack(
    template_args: list[Type], actual_args: list[Type], direction: int
) -> list[Constraint]:
    """Infer constraints between two lists of types with variadic items.

    This function is only supposed to be called when a variadic item is present in templates.
    If there is no variadic item the actuals, we simply use split_with_prefix_and_suffix()
    and infer prefix <: prefix, suffix <: suffix, variadic <: middle. If there is a variadic
    item in the actuals we need to be more careful, only common prefix/suffix can generate
    constraints, also we can only infer constraints for variadic template item, if template
    prefix/suffix are shorter that actual ones, otherwise there may be partial overlap
    between variadic items, for example if template prefix is longer:

        templates: T1, T2, Ts, Ts, Ts, ...
        actuals:   A1, As, As, As, ...

    Note: this function can only be called for builtin variadic constructors: Tuple and Callable.
    For instances, you should first find correct type argument mapping.
    """
    template_unpack = find_unpack_in_list(template_args)
    assert template_unpack is not None
    template_prefix = template_unpack
    template_suffix = len(template_args) - template_prefix - 1

    t_unpack = None
    res = []

    actual_unpack = find_unpack_in_list(actual_args)
    if actual_unpack is None:
        t_unpack = template_args[template_unpack]
        if template_prefix + template_suffix > len(actual_args):
            # These can't be subtypes of each-other, return fast.
            assert isinstance(t_unpack, UnpackType)
            if isinstance(t_unpack.type, TypeVarTupleType):
                # Set TypeVarTuple to empty to improve error messages.
                return [
                    Constraint(
                        t_unpack.type, direction, TupleType([], t_unpack.type.tuple_fallback)
                    )
                ]
            else:
                return []
        common_prefix = template_prefix
        common_suffix = template_suffix
    else:
        actual_prefix = actual_unpack
        actual_suffix = len(actual_args) - actual_prefix - 1
        common_prefix = min(template_prefix, actual_prefix)
        common_suffix = min(template_suffix, actual_suffix)
        if actual_prefix >= template_prefix and actual_suffix >= template_suffix:
            # This is the only case where we can guarantee there will be no partial overlap
            # (note however partial overlap is OK for variadic tuples, it is handled below).
            t_unpack = template_args[template_unpack]

    # Handle constraints from prefixes/suffixes first.
    start, middle, end = split_with_prefix_and_suffix(
        tuple(actual_args), common_prefix, common_suffix
    )
    for t, a in zip(template_args[:common_prefix], start):
        res.extend(infer_constraints(t, a, direction))
    if common_suffix:
        for t, a in zip(template_args[-common_suffix:], end):
            res.extend(infer_constraints(t, a, direction))

    if t_unpack is not None:
        # Add constraint(s) for variadic item when possible.
        assert isinstance(t_unpack, UnpackType)
        tp = get_proper_type(t_unpack.type)
        if isinstance(tp, Instance) and tp.type.fullname == "builtins.tuple":
            # Homogeneous case *tuple[T, ...] <: [X, Y, Z, ...].
            for a in middle:
                # TODO: should we use union instead of join here?
                if not isinstance(a, UnpackType):
                    res.extend(infer_constraints(tp.args[0], a, direction))
                else:
                    a_tp = get_proper_type(a.type)
                    # This is the case *tuple[T, ...] <: *tuple[A, ...].
                    if isinstance(a_tp, Instance) and a_tp.type.fullname == "builtins.tuple":
                        res.extend(infer_constraints(tp.args[0], a_tp.args[0], direction))
        elif isinstance(tp, TypeVarTupleType):
            res.append(Constraint(tp, direction, TupleType(list(middle), tp.tuple_fallback)))
    elif actual_unpack is not None:
        # A special case for a variadic tuple unpack, we simply infer T <: X from
        # Tuple[..., *tuple[T, ...], ...] <: Tuple[..., *tuple[X, ...], ...].
        actual_unpack_type = actual_args[actual_unpack]
        assert isinstance(actual_unpack_type, UnpackType)
        a_unpacked = get_proper_type(actual_unpack_type.type)
        if isinstance(a_unpacked, Instance) and a_unpacked.type.fullname == "builtins.tuple":
            t_unpack = template_args[template_unpack]
            assert isinstance(t_unpack, UnpackType)
            tp = get_proper_type(t_unpack.type)
            if isinstance(tp, Instance) and tp.type.fullname == "builtins.tuple":
                res.extend(infer_constraints(tp.args[0], a_unpacked.args[0], direction))
    return res

