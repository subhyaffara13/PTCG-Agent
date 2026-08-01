
def check_type_parameter(
    left: Type, right: Type, variance: int, proper_subtype: bool, subtype_context: SubtypeContext
) -> bool:
    # It is safe to consider empty collection literals and similar as covariant, since
    # such type can't be stored in a variable, see checker.is_valid_inferred_type().
    if variance == INVARIANT:
        p_left = get_proper_type(left)
        if isinstance(p_left, UninhabitedType) and p_left.ambiguous:
            variance = COVARIANT
    # If variance hasn't been inferred yet, we are lenient and default to
    # covariance. This shouldn't happen often, but it's very difficult to
    # avoid these cases altogether.
    if variance == COVARIANT or variance == VARIANCE_NOT_READY:
        if proper_subtype:
            return is_proper_subtype(left, right, subtype_context=subtype_context)
        else:
            return is_subtype(left, right, subtype_context=subtype_context)
    elif variance == CONTRAVARIANT:
        if proper_subtype:
            return is_proper_subtype(right, left, subtype_context=subtype_context)
        else:
            return is_subtype(right, left, subtype_context=subtype_context)
    else:
        if proper_subtype:
            # We pass ignore_promotions=False because it is a default for subtype checks.
            # The actual value will be taken from the subtype_context, and it is whatever
            # the original caller passed.
            return is_same_type(
                left, right, ignore_promotions=False, subtype_context=subtype_context
            )
        else:
            return is_equivalent(left, right, subtype_context=subtype_context)

