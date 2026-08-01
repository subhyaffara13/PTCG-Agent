
def is_proper_subtype(
    left: Type,
    right: Type,
    *,
    subtype_context: SubtypeContext | None = None,
    ignore_promotions: bool = False,
    erase_instances: bool = False,
    keep_erased_types: bool = False,
) -> bool:
    """Is left a proper subtype of right?

    For proper subtypes, there's no need to rely on compatibility due to
    Any types. Every usable type is a proper subtype of itself.

    If erase_instances is True, erase left instance *after* mapping it to supertype
    (this is useful for runtime isinstance() checks). If keep_erased_types is True,
    do not consider ErasedType a subtype of all types (used by type inference against unions).
    """
    if left == right:
        return True
    if subtype_context is None:
        subtype_context = SubtypeContext(
            ignore_promotions=ignore_promotions,
            erase_instances=erase_instances,
            keep_erased_types=keep_erased_types,
        )
    else:
        assert (
            not ignore_promotions and not erase_instances and not keep_erased_types
        ), "Don't pass both context and individual flags"
    if type_state.is_assumed_proper_subtype(left, right):
        return True
    if mypy.typeops.is_recursive_pair(left, right):
        # Same as for non-proper subtype, see detailed comment there for explanation.
        with pop_on_exit(type_state.get_assumptions(is_proper=True), left, right):
            return _is_subtype(left, right, subtype_context, proper_subtype=True)
    return _is_subtype(left, right, subtype_context, proper_subtype=True)

