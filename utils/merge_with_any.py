
def merge_with_any(constraint: Constraint) -> Constraint:
    """Transform a constraint target into a union with given Any type."""
    target = constraint.target
    if is_union_with_any(target):
        # Do not produce redundant unions.
        return constraint
    # TODO: if we will support multiple sources Any, use this here instead.
    any_type = AnyType(TypeOfAny.implementation_artifact)
    return Constraint(
        constraint.origin_type_var,
        constraint.op,
        UnionType.make_union([target, any_type], target.line, target.column),
    )

