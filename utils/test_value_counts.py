
def test_value_counts(index_or_series_obj):
    obj = index_or_series_obj
    obj = np.repeat(obj, range(1, len(obj) + 1))
    result = obj.value_counts()

    counter = collections.Counter(obj)
    expected = Series(dict(counter.most_common()), dtype=np.int64, name="count")

    if obj.dtype != np.float16:
        expected.index = expected.index.astype(obj.dtype)
    else:
        with pytest.raises(NotImplementedError, match="float16 indexes are not "):
            expected.index.astype(obj.dtype)
        return
    if isinstance(expected.index, MultiIndex):
        expected.index.names = obj.names
    else:
        expected.index.name = obj.name

    if not isinstance(result.dtype, np.dtype):
        if getattr(obj.dtype, "storage", "") == "pyarrow":
            expected = expected.astype("int64[pyarrow]")
        else:
            # i.e IntegerDtype
            expected = expected.astype("Int64")

    tm.assert_series_equal(result, expected)


def test_value_counts(sort, dropna, ascending, normalize, rng):
    ri = RangeIndex(rng, name="A")
    result = ri.value_counts(
        normalize=normalize, sort=sort, ascending=ascending, dropna=dropna
    )
    expected = Index(list(rng), name="A").value_counts(
        normalize=normalize, sort=sort, ascending=ascending, dropna=dropna
    )
    tm.assert_series_equal(result, expected, check_index_type=False)

