
def pre_validate_solutions(
    solutions: list[Type | None],
    original_vars: Sequence[TypeVarLikeType],
    constraints: list[Constraint],
) -> list[Type | None]:
    """Check is each solution satisfies the upper bound of the corresponding type variable.

    If it doesn't satisfy the bound, check if bound itself satisfies all constraints, and
    if yes, use it instead as a fallback solution.
    """
    new_solutions: list[Type | None] = []
    for t, s in zip(original_vars, solutions):
        if is_callable_protocol(t.upper_bound):
            # This is really ad-hoc, but a proper fix would be much more complex,
            # and otherwise this may cause crash in a relatively common scenario.
            new_solutions.append(s)
            continue
        if s is not None and not is_subtype(s, t.upper_bound):
            bound_satisfies_all = True
            for c in constraints:
                if c.op == SUBTYPE_OF and not is_subtype(t.upper_bound, c.target):
                    bound_satisfies_all = False
                    break
                if c.op == SUPERTYPE_OF and not is_subtype(c.target, t.upper_bound):
                    bound_satisfies_all = False
                    break
            if bound_satisfies_all:
                new_solutions.append(t.upper_bound)
                continue
        new_solutions.append(s)
    return new_solutions

