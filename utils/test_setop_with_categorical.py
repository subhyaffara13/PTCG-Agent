
def test_setop_with_categorical(index_flat, sort, method, using_infer_string):
    # MultiIndex tested separately in tests.indexes.multi.test_setops
    index = index_flat

    other = index.astype("category")
    exact = "equiv" if isinstance(index, RangeIndex) else True

    result = getattr(index, method)(other, sort=sort)
    expected = getattr(index, method)(index, sort=sort)
    if (
        using_infer_string
        and index.empty
        and method in ("union", "symmetric_difference")
    ):
        expected = expected.astype("category")
    tm.assert_index_equal(result, expected, exact=exact)

    result = getattr(index, method)(other[:5], sort=sort)
    expected = getattr(index, method)(index[:5], sort=sort)
    if (
        using_infer_string
        and index.empty
        and method in ("union", "symmetric_difference")
    ):
        expected = expected.astype("category")
    tm.assert_index_equal(result, expected, exact=exact)


def test_setop_with_categorical(idx, sort, method):
    other = idx.to_flat_index().astype("category")
    res_names = [None] * idx.nlevels

    result = getattr(idx, method)(other, sort=sort)
    expected = getattr(idx, method)(idx, sort=sort).rename(res_names)
    tm.assert_index_equal(result, expected)

    result = getattr(idx, method)(other[:5], sort=sort)
    expected = getattr(idx, method)(idx[:5], sort=sort).rename(res_names)
    tm.assert_index_equal(result, expected)

