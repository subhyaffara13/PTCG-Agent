
def assert_metadata_equivalent(
    left: DataFrame | Series, right: DataFrame | Series | None = None
) -> None:
    """
    Check that ._metadata attributes are equivalent.
    """
    for attr in left._metadata:
        val = getattr(left, attr, None)
        if right is None:
            assert val is None
        else:
            assert val == getattr(right, attr, None)

