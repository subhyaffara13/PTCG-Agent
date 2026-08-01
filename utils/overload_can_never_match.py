
def overload_can_never_match(signature: CallableType, other: CallableType) -> bool:
    """Check if the 'other' method can never be matched due to 'signature'.

    This can happen if signature's parameters are all strictly broader then
    other's parameters.

    Assumes that both signatures have overlapping argument counts.
    """
    # The extra erasure is needed to prevent spurious errors
    # in situations where an `Any` overload is used as a fallback
    # for an overload with type variables. The spurious error appears
    # because the type variables turn into `Any` during unification in
    # the below subtype check and (surprisingly?) `is_proper_subtype(Any, Any)`
    # returns `True`.
    # TODO: find a cleaner solution instead of this ad-hoc erasure.
    exp_signature = expand_type(
        signature, {tvar.id: erase_def_to_union_or_bound(tvar) for tvar in signature.variables}
    )
    return is_callable_compatible(
        exp_signature, other, is_compat=is_more_precise, is_proper_subtype=True, ignore_return=True
    )

