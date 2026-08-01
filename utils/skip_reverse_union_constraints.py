
def skip_reverse_union_constraints(cs: list[Constraint]) -> list[Constraint]:
    """Avoid ambiguities for constraints inferred from unions during polymorphic inference.

    Polymorphic inference implicitly relies on assumption that a reverse of a linear constraint
    is a linear constraint. This is however not true in presence of union types, for example
    T :> Union[S, int] vs S <: T. Trying to solve such constraints would be detected ambiguous
    as (T, S) form a non-linear SCC. However, simply removing the linear part results in a valid
    solution T = Union[S, int], S = <free>. A similar scenario is when we get T <: Union[T, int],
    such constraints carry no information, and will equally confuse linearity check.

    TODO: a cleaner solution may be to avoid inferring such constraints in first place, but
    this would require passing around a flag through all infer_constraints() calls.
    """
    reverse_union_cs = set()
    for c in cs:
        p_target = get_proper_type(c.target)
        if isinstance(p_target, UnionType):
            for item in p_target.items:
                if isinstance(item, TypeVarType):
                    if item == c.origin_type_var and c.op == SUBTYPE_OF:
                        reverse_union_cs.add(c)
                        continue
                    # These two forms are semantically identical, but are different from
                    # the point of view of Constraint.__eq__().
                    reverse_union_cs.add(Constraint(item, neg_op(c.op), c.origin_type_var))
                    reverse_union_cs.add(Constraint(c.origin_type_var, c.op, item))
    return [c for c in cs if c not in reverse_union_cs]

