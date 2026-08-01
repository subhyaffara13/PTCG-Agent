
def infer_type_arguments(
    type_vars: Sequence[TypeVarLikeType],
    template: Type,
    actual: Type,
    is_supertype: bool = False,
    skip_unsatisfied: bool = False,
    erase_types: bool = True,
) -> list[Type | None]:
    # Like infer_function_type_arguments, but only match a single type
    # against a generic type.
    constraints = infer_constraints(
        template, actual, SUPERTYPE_OF if is_supertype else SUBTYPE_OF, erase_types=erase_types
    )
    return solve_constraints(type_vars, constraints, skip_unsatisfied=skip_unsatisfied)[0]

