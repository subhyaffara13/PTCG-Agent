
def match_generic_callables(t: CallableType, s: CallableType) -> tuple[CallableType, CallableType]:
    # The case where we combine/join/meet similar callables, situation where both are generic
    # requires special care. A more principled solution may involve unify_generic_callable(),
    # but it would have two problems:
    #   * This adds risk of infinite recursion: e.g. join -> unification -> solver -> join
    #   * Using unification is an incorrect thing for meets, as it "widens" the types
    # Finally, this effectively falls back to an old behaviour before namespaces were added to
    # type variables, and it worked relatively well.
    max_len = max(len(t.variables), len(s.variables))
    min_len = min(len(t.variables), len(s.variables))
    if min_len == 0:
        return t, s
    new_ids = [TypeVarId.new(meta_level=0) for _ in range(max_len)]
    # Note: this relies on variables being in order they appear in function definition.
    return update_callable_ids(t, new_ids), update_callable_ids(s, new_ids)

