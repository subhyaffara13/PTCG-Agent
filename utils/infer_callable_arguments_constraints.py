
def infer_callable_arguments_constraints(
    template: NormalizedCallableType | Parameters,
    actual: NormalizedCallableType | Parameters,
    direction: int,
) -> list[Constraint]:
    """Infer constraints between argument types of two callables.

    This function essentially extracts four steps from are_parameters_compatible() in
    subtypes.py that involve subtype checks between argument types. We keep the argument
    matching logic, but ignore various strictness flags present there, and checks that
    do not involve subtyping. Then in place of every subtype check we put an infer_constraints()
    call for the same types.
    """
    res = []
    if direction == SUBTYPE_OF:
        left, right = template, actual
    else:
        left, right = actual, template
    left_star = left.var_arg()
    left_star2 = left.kw_arg()
    right_star = right.var_arg()
    right_star2 = right.kw_arg()

    # Numbering of steps below matches the one in are_parameters_compatible() for convenience.
    # Phase 1a: compare star vs star arguments.
    if left_star is not None and right_star is not None:
        res.extend(infer_directed_arg_constraints(left_star.typ, right_star.typ, direction))
    if left_star2 is not None and right_star2 is not None:
        res.extend(infer_directed_arg_constraints(left_star2.typ, right_star2.typ, direction))

    # Phase 1b: compare left args with corresponding non-star right arguments.
    for right_arg in right.formal_arguments():
        left_arg = mypy.typeops.callable_corresponding_argument(left, right_arg)
        if left_arg is None:
            continue
        res.extend(infer_directed_arg_constraints(left_arg.typ, right_arg.typ, direction))

    # Phase 1c: compare left args with right *args.
    if right_star is not None:
        right_by_position = right.try_synthesizing_arg_from_vararg(None)
        assert right_by_position is not None
        i = right_star.pos
        assert i is not None
        while i < len(left.arg_kinds) and left.arg_kinds[i].is_positional():
            left_by_position = left.argument_by_position(i)
            assert left_by_position is not None
            res.extend(
                infer_directed_arg_constraints(
                    left_by_position.typ, right_by_position.typ, direction
                )
            )
            i += 1

    # Phase 1d: compare left args with right **kwargs.
    if right_star2 is not None:
        right_names = {name for name in right.arg_names if name is not None}
        left_only_names = set()
        for name, kind in zip(left.arg_names, left.arg_kinds):
            if name is None or kind.is_star() or name in right_names:
                continue
            left_only_names.add(name)

        right_by_name = right.try_synthesizing_arg_from_kwarg(None)
        assert right_by_name is not None
        for name in left_only_names:
            left_by_name = left.argument_by_name(name)
            assert left_by_name is not None
            res.extend(
                infer_directed_arg_constraints(left_by_name.typ, right_by_name.typ, direction)
            )
    return res

