
def _validate_link(*tuples: t.Any) -> None:
    """Validate arguments for traitlet link functions"""
    for tup in tuples:
        if not len(tup) == 2:
            raise TypeError(
                "Each linked traitlet must be specified as (HasTraits, 'trait_name'), not %r" % t
            )
        obj, trait_name = tup
        if not isinstance(obj, HasTraits):
            raise TypeError("Each object must be HasTraits, not %r" % type(obj))
        if trait_name not in obj.traits():
            raise TypeError(f"{obj!r} has no trait {trait_name!r}")

