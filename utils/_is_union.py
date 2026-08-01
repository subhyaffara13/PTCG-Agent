
def _is_union(field_type: type) -> bool:
    # NOTE: types.UnionType for `T | U`, typing.Union for `Union[T, U]`.
    # TODO: Drop the `hasattr()` once the minimum supported Python version
    # is >= 3.10.
    union_types = (
        (types.UnionType, typing.Union)
        if hasattr(types, "UnionType")
        else (typing.Union,)
    )
    return typing.get_origin(field_type) in union_types

