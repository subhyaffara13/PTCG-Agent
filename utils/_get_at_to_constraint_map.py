
def _get_at_to_constraint_map() -> dict[type, str]:
    """Return a mapping of annotated types to constraints.

    Normally, we would define a mapping like this in the module scope, but we can't do that
    because we don't permit module level imports of `annotated_types`, in an attempt to speed up
    the import time of `pydantic`. We still only want to have this dictionary defined in one place,
    so we use this function to cache the result.
    """
    import annotated_types as at

    return {
        at.Gt: 'gt',
        at.Ge: 'ge',
        at.Lt: 'lt',
        at.Le: 'le',
        at.MultipleOf: 'multiple_of',
        at.MinLen: 'min_length',
        at.MaxLen: 'max_length',
    }

