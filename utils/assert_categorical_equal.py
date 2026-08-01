
def assert_categorical_equal(
    left,
    right,
    check_dtype: bool = True,
    check_category_order: bool = True,
    obj: str = "Categorical",
) -> None:
    """
    Test that Categoricals are equivalent.

    Parameters
    ----------
    left : Categorical
    right : Categorical
    check_dtype : bool, default True
        Check that integer dtype of the codes are the same.
    check_category_order : bool, default True
        Whether the order of the categories should be compared, which
        implies identical integer codes.  If False, only the resulting
        values are compared.  The ordered attribute is
        checked regardless.
    obj : str, default 'Categorical'
        Specify object name being compared, internally used to show appropriate
        assertion message.
    """
    _check_isinstance(left, right, Categorical)

    exact: bool | str
    if isinstance(left.categories, RangeIndex) or isinstance(
        right.categories, RangeIndex
    ):
        exact = "equiv"
    else:
        # We still want to require exact matches for Index
        exact = True

    if check_category_order:
        assert_index_equal(
            left.categories, right.categories, obj=f"{obj}.categories", exact=exact
        )
        assert_numpy_array_equal(
            left.codes, right.codes, check_dtype=check_dtype, obj=f"{obj}.codes"
        )
    else:
        try:
            lc = left.categories.sort_values()
            rc = right.categories.sort_values()
        except TypeError:
            # e.g. '<' not supported between instances of 'int' and 'str'
            lc, rc = left.categories, right.categories
        assert_index_equal(lc, rc, obj=f"{obj}.categories", exact=exact)
        assert_index_equal(
            left.categories.take(left.codes),
            right.categories.take(right.codes),
            obj=f"{obj}.values",
            exact=exact,
        )

    assert_attr_equal("ordered", left, right, obj=obj)

