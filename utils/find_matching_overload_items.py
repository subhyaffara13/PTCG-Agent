
def find_matching_overload_items(
    overloaded: Overloaded, template: CallableType
) -> list[CallableType]:
    """Like find_matching_overload_item, but return all matches, not just the first."""
    items = overloaded.items
    res = []
    for item in items:
        # Return type may be indeterminate in the template, so ignore it when performing a
        # subtype check.
        if mypy.subtypes.is_callable_compatible(
            item,
            template,
            is_compat=mypy.subtypes.is_subtype,
            is_proper_subtype=False,
            ignore_return=True,
        ):
            res.append(item)
    if not res:
        # Falling back to all items if we can't find a match is pretty arbitrary, but
        # it maintains backward compatibility.
        res = items.copy()
    return res

