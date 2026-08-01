
def find_matching_overload_item(overloaded: Overloaded, template: CallableType) -> CallableType:
    """Disambiguate overload item against a template."""
    items = overloaded.items
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
            return item
    # Fall back to the first item if we can't find a match. This is totally arbitrary --
    # maybe we should just bail out at this point.
    return items[0]

