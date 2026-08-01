
def add_secondary_constraints(cs: set[Constraint], lower: Type, upper: Type) -> None:
    """Add secondary constraints inferred between lower and upper (in place)."""
    if isinstance(get_proper_type(upper), UnionType) and isinstance(
        get_proper_type(lower), UnionType
    ):
        # When both types are unions, this can lead to inferring spurious constraints,
        # for example Union[T, int] <: S <: Union[T, int] may infer T <: int.
        # To avoid this, just skip them for now.
        return
    # TODO: what if secondary constraints result in inference against polymorphic actual?
    cs.update(set(infer_constraints(lower, upper, SUBTYPE_OF)))
    cs.update(set(infer_constraints(upper, lower, SUPERTYPE_OF)))

