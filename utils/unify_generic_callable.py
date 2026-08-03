from typing import Any

def unify_generic_callable(
    type: NormalizedCallableType,
    target: NormalizedCallableType,
    ignore_return: bool,
    return_constraint_direction: int | None = None,
) -> NormalizedCallableType | None:
    """Try to unify a generic callable type with another callable type.

    Return unified CallableType if successful; otherwise, return None.
    """
    import mypy.solve

    if set(type.type_var_ids()) & {v.id for v in mypy.typeops.get_all_type_vars(target)}:
        # Overload overlap check does nasty things like unifying in opposite direction.
        # This can easily create type variable clashes, so we need to refresh.
        type = freshen_function_type_vars(type)

    if return_constraint_direction is None:
        return_constraint_direction = mypy.constraints.SUBTYPE_OF

    constraints: list[mypy.constraints.Constraint] = []
    # There is some special logic for inference in callables, so better use them
    # as wholes instead of picking separate arguments.
    cs = mypy.constraints.infer_constraints(
        type.copy_modified(ret_type=UninhabitedType()),
        target.copy_modified(ret_type=UninhabitedType()),
        mypy.constraints.SUBTYPE_OF,
        skip_neg_op=True,
    )
    constraints.extend(cs)
    if not ignore_return:
        c = mypy.constraints.infer_constraints(
            type.ret_type, target.ret_type, return_constraint_direction
        )
        constraints.extend(c)
    inferred_vars, _ = mypy.solve.solve_constraints(
        type.variables, constraints, allow_polymorphic=True
    )
    if None in inferred_vars:
        return None
    non_none_inferred_vars = cast(list[Type], inferred_vars)
    had_errors = False

    def report(*args: Any) -> None:
        nonlocal had_errors
        had_errors = True

    # This function may be called by the solver, so we need to allow erased types here.
    # We anyway allow checking subtyping between other types containing <Erased>
    # (probably also because solver needs subtyping). See also comment in
    # ExpandTypeVisitor.visit_erased_type().
    applied = mypy.applytype.apply_generic_arguments(
        type, non_none_inferred_vars, report, context=target
    )
    if had_errors:
        return None
    return cast(NormalizedCallableType, applied)

