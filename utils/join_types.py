
def join_types(
    s: ProperType, t: ProperType, instance_joiner: InstanceJoiner | None = None
) -> ProperType: ...


def join_types(s: Type, t: Type, instance_joiner: InstanceJoiner | None = None) -> Type: ...


def join_types(s: Type, t: Type, instance_joiner: InstanceJoiner | None = None) -> Type:
    """Return the least upper bound of s and t.

    For example, the join of 'int' and 'object' is 'object'.
    """
    if mypy.typeops.is_recursive_pair(s, t):
        # This case can trigger an infinite recursion, general support for this will be
        # tricky so we use a trivial join (like for protocols).
        return trivial_join(s, t)
    s = get_proper_type(s)
    t = get_proper_type(t)

    if (s.can_be_true, s.can_be_false) != (t.can_be_true, t.can_be_false):
        # if types are restricted in different ways, use the more general versions
        s = mypy.typeops.true_or_false(s)
        t = mypy.typeops.true_or_false(t)

    if isinstance(s, UnionType) and not isinstance(t, UnionType):
        s, t = t, s

    if isinstance(s, AnyType):
        return s

    if isinstance(s, ErasedType):
        return t

    if isinstance(s, NoneType) and not isinstance(t, NoneType):
        s, t = t, s

    if isinstance(s, UninhabitedType) and not isinstance(t, UninhabitedType):
        s, t = t, s

    # Meets/joins require callable type normalization.
    s, t = normalize_callables(s, t)

    # Use a visitor to handle non-trivial cases.
    return t.accept(TypeJoinVisitor(s, instance_joiner))

