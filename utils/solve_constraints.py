
def solve_constraints(
    original_vars: Sequence[TypeVarLikeType],
    constraints: list[Constraint],
    strict: bool = True,
    allow_polymorphic: bool = False,
    skip_unsatisfied: bool = False,
) -> tuple[list[Type | None], list[TypeVarLikeType]]:
    """Solve type constraints.

    Return the best type(s) for type variables; each type can be None if the value of
    the variable could not be solved.

    If a variable has no constraints, if strict=True then arbitrarily
    pick UninhabitedType as the value of the type variable. If strict=False, pick AnyType.
    If allow_polymorphic=True, then use the full algorithm that can potentially return
    free type variables in solutions (these require special care when applying). Otherwise,
    use a simplified algorithm that just solves each type variable individually if possible.

    The skip_unsatisfied flag matches the same one in applytype.apply_generic_arguments().
    """
    vars = [tv.id for tv in original_vars]
    if not vars:
        return [], []

    originals = {tv.id: tv for tv in original_vars}
    extra_vars: list[TypeVarId] = []
    # Get additional type variables from generic actuals.
    for c in constraints:
        extra_vars.extend([v.id for v in c.extra_tvars if v.id not in vars + extra_vars])
        originals.update({v.id: v for v in c.extra_tvars if v.id not in originals})

    if allow_polymorphic:
        # Constraints inferred from unions require special handling in polymorphic inference.
        constraints = skip_reverse_union_constraints(constraints)

    # Collect a list of constraints for each type variable.
    cmap: dict[TypeVarId, list[Constraint]] = {tv: [] for tv in vars + extra_vars}
    for con in constraints:
        if con.type_var in vars + extra_vars:
            cmap[con.type_var].append(con)

    if allow_polymorphic:
        if constraints:
            solutions, free_vars = solve_with_dependent(
                vars + extra_vars, constraints, vars, originals
            )
        else:
            solutions = {}
            free_vars = []
    else:
        solutions = {}
        free_vars = []
        for tv, cs in cmap.items():
            if not cs:
                continue
            lowers = [c.target for c in cs if c.op == SUPERTYPE_OF]
            uppers = [c.target for c in cs if c.op == SUBTYPE_OF]
            solution = solve_one(lowers, uppers)

            # Do not leak type variables in non-polymorphic solutions.
            if solution is None or not get_vars(
                solution, [tv for tv in extra_vars if tv not in vars]
            ):
                solutions[tv] = solution

    res: list[Type | None] = []
    for v in vars:
        if v in solutions:
            res.append(solutions[v])
        else:
            # No constraints for type variable -- 'UninhabitedType' is the most specific type.
            candidate: Type
            if strict:
                candidate = UninhabitedType()
                candidate.ambiguous = True
            else:
                candidate = AnyType(TypeOfAny.special_form)
            res.append(candidate)

    if not free_vars and not skip_unsatisfied:
        # Most of the validation for solutions is done in applytype.py, but here we can
        # quickly test solutions w.r.t. to upper bounds, and use the latter (if possible),
        # if solutions are actually not valid (due to poor inference context).
        res = pre_validate_solutions(res, original_vars, constraints)

    return res, free_vars

