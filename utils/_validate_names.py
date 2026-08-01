
def _validate_names(typename, field_names, extra_field_names):
    """
    Ensure that all the given names are valid Python identifiers that
    do not start with '_'.  Also check that there are no duplicates
    among field_names + extra_field_names.
    """
    for name in [typename] + field_names + extra_field_names:
        if not isinstance(name, str):
            raise TypeError('typename and all field names must be strings')
        if not name.isidentifier():
            raise ValueError('typename and all field names must be valid '
                             f'identifiers: {name!r}')
        if _iskeyword(name):
            raise ValueError('typename and all field names cannot be a '
                             f'keyword: {name!r}')

    seen = set()
    for name in field_names + extra_field_names:
        if name.startswith('_'):
            raise ValueError('Field names cannot start with an underscore: '
                             f'{name!r}')
        if name in seen:
            raise ValueError(f'Duplicate field name: {name!r}')
        seen.add(name)


def _validate_names(names: Sequence[Hashable] | None) -> None:
    """
    Raise ValueError if the `names` parameter contains duplicates or has an
    invalid data type.

    Parameters
    ----------
    names : array-like or None
        An array containing a list of the names used for the output DataFrame.

    Raises
    ------
    ValueError
        If names are not unique or are not ordered (e.g. set).
    """
    if names is not None:
        if len(names) != len(set(names)):
            raise ValueError("Duplicate names are not allowed.")
        if not (
            is_list_like(names, allow_sets=False) or isinstance(names, abc.KeysView)
        ):
            raise ValueError("Names should be an ordered collection.")

