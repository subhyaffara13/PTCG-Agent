
def infer_constraints_if_possible(
    template: Type, actual: Type, direction: int
) -> list[Constraint] | None:
    """Like infer_constraints, but return None if the input relation is
    known to be unsatisfiable, for example if template=List[T] and actual=int.
    (In this case infer_constraints would return [], just like it would for
    an automatically satisfied relation like template=List[T] and actual=object.)
    """
    if direction == SUBTYPE_OF and not mypy.subtypes.is_subtype(erase_typevars(template), actual):
        return None
    if direction == SUPERTYPE_OF and not mypy.subtypes.is_subtype(
        actual, erase_typevars(template)
    ):
        return None
    if (
        direction == SUPERTYPE_OF
        and isinstance(template, TypeVarType)
        and not mypy.subtypes.is_subtype(actual, erase_typevars(template.upper_bound))
    ):
        # This is not caught by the above branch because of the erase_typevars() call,
        # that would return 'Any' for a type variable.
        return None
    return infer_constraints(template, actual, direction)

