
def are_parameters_compatible(
    left: Parameters | NormalizedCallableType,
    right: Parameters | NormalizedCallableType,
    *,
    is_compat: Callable[[Type, Type], bool],
    is_proper_subtype: bool,
    ignore_pos_arg_names: bool = False,
    allow_partial_overlap: bool = False,
    strict_concatenate_check: bool = False,
) -> bool:
    """Helper function for is_callable_compatible, used for Parameter compatibility"""
    if right.is_ellipsis_args and not is_proper_subtype:
        return True

    left_star = left.var_arg()
    left_star2 = left.kw_arg()
    right_star = right.var_arg()
    right_star2 = right.kw_arg()

    # Treat "def _(*a: Any, **kw: Any) -> X" similarly to "Callable[..., X]"
    if are_trivial_parameters(right) and not is_proper_subtype:
        return True
    trivial_suffix = is_trivial_suffix(right) and not is_proper_subtype

    trivial_vararg_suffix = False
    if (
        right.arg_kinds[-1:] == [ARG_STAR]
        and isinstance(get_proper_type(right.arg_types[-1]), AnyType)
        and not is_proper_subtype
        and all(k.is_positional(star=True) for k in left.arg_kinds)
    ):
        # Similar to how (*Any, **Any) is considered a supertype of all callables, we consider
        # (*Any) a supertype of all callables with positional arguments. This is needed in
        # particular because we often refuse to try type inference if actual type is not
        # a subtype of erased template type.
        trivial_vararg_suffix = True

    # Match up corresponding arguments and check them for compatibility. In
    # every pair (argL, argR) of corresponding arguments from L and R, argL must
    # be "more general" than argR if L is to be a subtype of R.

    # Arguments are corresponding if they either share a name, share a position,
    # or both. If L's corresponding argument is ambiguous, L is not a subtype of R.

    # If left has one corresponding argument by name and another by position,
    # consider them to be one "merged" argument (and not ambiguous) if they're
    # both optional, they're name-only and position-only respectively, and they
    # have the same type.  This rule allows functions with (*args, **kwargs) to
    # properly stand in for the full domain of formal arguments that they're
    # used for in practice.

    # Every argument in R must have a corresponding argument in L, and every
    # required argument in L must have a corresponding argument in R.

    # Phase 1: Confirm every argument in R has a corresponding argument in L.

    # Phase 1a: If left and right can both accept an infinite number of args,
    #           their types must be compatible.
    #
    #           Furthermore, if we're checking for compatibility in all cases,
    #           we confirm that if R accepts an infinite number of arguments,
    #           L must accept the same.
    def _incompatible(left_arg: FormalArgument | None, right_arg: FormalArgument | None) -> bool:
        if right_arg is None:
            return False
        if left_arg is None:
            return not allow_partial_overlap and not trivial_suffix
        return not is_compat(right_arg.typ, left_arg.typ)

    if (
        _incompatible(left_star, right_star)
        and not trivial_vararg_suffix
        or _incompatible(left_star2, right_star2)
    ):
        return False

    # Phase 1b: Check non-star args: for every arg right can accept, left must
    #           also accept. The only exception is if we are allowing partial
    #           overlaps: in that case, we ignore optional args on the right.
    for right_arg in right.formal_arguments():
        left_arg = mypy.typeops.callable_corresponding_argument(left, right_arg)
        if left_arg is None:
            if allow_partial_overlap and not right_arg.required:
                continue
            return False
        if not are_args_compatible(
            left_arg,
            right_arg,
            is_compat,
            ignore_pos_arg_names=ignore_pos_arg_names,
            allow_partial_overlap=allow_partial_overlap,
            allow_imprecise_kinds=right.imprecise_arg_kinds,
        ):
            return False

    if trivial_suffix:
        # For trivial right suffix we *only* check that every non-star right argument
        # has a valid match on the left.
        return True

    # Phase 1c: Check var args. Right has an infinite series of optional positional
    #           arguments. Get all further positional args of left, and make sure
    #           they're more general than the corresponding member in right.
    # TODO: handle suffix in UnpackType (i.e. *args: *Tuple[Ts, X, Y]).
    if right_star is not None and not trivial_vararg_suffix:
        # Synthesize an anonymous formal argument for the right
        right_by_position = right.try_synthesizing_arg_from_vararg(None)
        assert right_by_position is not None

        i = right_star.pos
        assert i is not None
        while i < len(left.arg_kinds) and left.arg_kinds[i].is_positional():
            if allow_partial_overlap and left.arg_kinds[i].is_optional():
                break

            left_by_position = left.argument_by_position(i)
            assert left_by_position is not None

            if not are_args_compatible(
                left_by_position,
                right_by_position,
                is_compat,
                ignore_pos_arg_names=ignore_pos_arg_names,
                allow_partial_overlap=allow_partial_overlap,
            ):
                return False
            i += 1

    # Phase 1d: Check kw args. Right has an infinite series of optional named
    #           arguments. Get all further named args of left, and make sure
    #           they're more general than the corresponding member in right.
    if right_star2 is not None:
        right_names = {name for name in right.arg_names if name is not None}
        left_only_names = set()
        for name, kind in zip(left.arg_names, left.arg_kinds):
            if (
                name is None
                or kind.is_star()
                or name in right_names
                or not strict_concatenate_check
            ):
                continue
            left_only_names.add(name)

        # Synthesize an anonymous formal argument for the right
        right_by_name = right.try_synthesizing_arg_from_kwarg(None)
        assert right_by_name is not None

        for name in left_only_names:
            left_by_name = left.argument_by_name(name)
            assert left_by_name is not None

            if allow_partial_overlap and not left_by_name.required:
                continue

            if not are_args_compatible(
                left_by_name,
                right_by_name,
                is_compat,
                ignore_pos_arg_names=ignore_pos_arg_names,
                allow_partial_overlap=allow_partial_overlap,
            ):
                return False

    # Phase 2: Left must not impose additional restrictions.
    #          (Every required argument in L must have a corresponding argument in R)
    #          Note: we already checked the *arg and **kwarg arguments in phase 1a.
    for left_arg in left.formal_arguments():
        right_by_name = (
            right.argument_by_name(left_arg.name) if left_arg.name is not None else None
        )

        right_by_pos = (
            right.argument_by_position(left_arg.pos) if left_arg.pos is not None else None
        )

        # If the left hand argument corresponds to two right-hand arguments,
        # neither of them can be required.
        if (
            right_by_name is not None
            and right_by_pos is not None
            and right_by_name != right_by_pos
            and (right_by_pos.required or right_by_name.required)
            and strict_concatenate_check
            and not right.imprecise_arg_kinds
        ):
            return False

        # All *required* left-hand arguments must have a corresponding
        # right-hand argument.  Optional args do not matter.
        if left_arg.required and right_by_pos is None and right_by_name is None:
            return False

    return True

