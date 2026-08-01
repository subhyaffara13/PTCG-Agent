
def is_unsafe_overlapping_overload_signatures(
    signature: CallableType,
    other: CallableType,
    class_type_vars: list[TypeVarLikeType],
    partial_only: bool = True,
) -> bool:
    """Check if two overloaded signatures are unsafely overlapping or partially overlapping.

    We consider two functions 's' and 't' to be unsafely overlapping if three
    conditions hold:

    1.  s's parameters are partially overlapping with t's. i.e. there are calls that are
        valid for both signatures.
    2.  for these common calls, some of t's parameters types are wider that s's.
    3.  s's return type is NOT a subset of t's.

    Note that we use subset rather than subtype relationship in these checks because:
    * Overload selection happens at runtime, not statically.
    * This results in more lenient behavior.
    This can cause false negatives (e.g. if overloaded function returns an externally
    visible attribute with invariant type), but such situations are rare. In general,
    overloads in Python are generally unsafe, so we intentionally try to avoid giving
    non-actionable errors (see more details in comments below).

    Assumes that 'signature' appears earlier in the list of overload
    alternatives then 'other' and that their argument counts are overlapping.
    """
    # Try detaching callables from the containing class so that all TypeVars
    # are treated as being free, i.e. the signature is as seen from inside the class,
    # where "self" is not yet bound to anything.
    signature = detach_callable(signature, class_type_vars)
    other = detach_callable(other, class_type_vars)

    # Note: We repeat this check twice in both directions compensate for slight
    # asymmetries in 'is_callable_compatible'.

    other_expanded = expand_callable_variants(other)
    for sig_variant in expand_callable_variants(signature):
        for other_variant in other_expanded:
            # Using only expanded callables may cause false negatives, we can add
            # more variants (e.g. using inference between callables) in the future.
            if is_subset_no_promote(sig_variant.ret_type, other_variant.ret_type):
                continue
            if not (
                is_callable_compatible(
                    sig_variant,
                    other_variant,
                    is_compat=is_overlapping_types_for_overload,
                    check_args_covariantly=False,
                    is_proper_subtype=False,
                    is_compat_return=lambda l, r: not is_subset_no_promote(l, r),
                    allow_partial_overlap=True,
                )
                or is_callable_compatible(
                    other_variant,
                    sig_variant,
                    is_compat=is_overlapping_types_for_overload,
                    check_args_covariantly=True,
                    is_proper_subtype=False,
                    is_compat_return=lambda l, r: not is_subset_no_promote(r, l),
                    allow_partial_overlap=True,
                )
            ):
                continue
            # Using the same `allow_partial_overlap` flag as before, can cause false
            # negatives in case where star argument is used in a catch-all fallback overload.
            # But again, practicality beats purity here.
            if not partial_only or not is_callable_compatible(
                other_variant,
                sig_variant,
                is_compat=is_subset_no_promote,
                check_args_covariantly=True,
                is_proper_subtype=False,
                ignore_return=True,
                allow_partial_overlap=True,
            ):
                return True
    return False

