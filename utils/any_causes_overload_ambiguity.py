
def any_causes_overload_ambiguity(
    items: list[CallableType],
    return_types: list[Type],
    arg_types: list[Type],
    arg_kinds: list[ArgKind],
    arg_names: Sequence[str | None] | None,
) -> bool:
    """May an argument containing 'Any' cause ambiguous result type on call to overloaded function?

    Note that this sometimes returns True even if there is no ambiguity, since a correct
    implementation would be complex (and the call would be imprecisely typed due to Any
    types anyway).

    Args:
        items: Overload items matching the actual arguments
        arg_types: Actual argument types
        arg_kinds: Actual argument kinds
        arg_names: Actual argument names
    """
    if all_same_types(return_types):
        return False

    actual_to_formal = [
        map_formals_to_actuals(
            arg_kinds, arg_names, item.arg_kinds, item.arg_names, lambda i: arg_types[i]
        )
        for item in items
    ]

    for arg_idx, arg_type in enumerate(arg_types):
        # We ignore Anys in type object callables as ambiguity
        # creators, since that can lead to falsely claiming ambiguity
        # for overloads between Type and Callable.
        if has_any_type(arg_type, ignore_in_type_obj=True):
            matching_formals_unfiltered = [
                (item_idx, lookup[arg_idx])
                for item_idx, lookup in enumerate(actual_to_formal)
                if lookup[arg_idx]
            ]

            matching_returns = []
            matching_formals = []
            for item_idx, formals in matching_formals_unfiltered:
                matched_callable = items[item_idx]
                matching_returns.append(matched_callable.ret_type)

                # Note: if an actual maps to multiple formals of differing types within
                # a single callable, then we know at least one of those formals must be
                # a different type then the formal(s) in some other callable.
                # So it's safe to just append everything to the same list.
                for formal in formals:
                    matching_formals.append(matched_callable.arg_types[formal])
            if not all_same_types(matching_formals) and not all_same_types(matching_returns):
                # Any maps to multiple different types, and the return types of these items differ.
                return True
    return False

