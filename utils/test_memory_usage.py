import sys

def test_memory_usage(index_or_series_memory_obj):
    obj = index_or_series_memory_obj
    # Clear index caches so that len(obj) == 0 report 0 memory usage
    if isinstance(obj, Series):
        is_ser = True
        obj.index._engine.clear_mapping()
    else:
        is_ser = False
        obj._engine.clear_mapping()

    res = obj.memory_usage()
    res_deep = obj.memory_usage(deep=True)

    def _is_object_dtype(obj):
        if isinstance(obj, pd.MultiIndex):
            return any(_is_object_dtype(level) for level in obj.levels)
        elif isinstance(obj.dtype, pd.CategoricalDtype):
            return _is_object_dtype(obj.dtype.categories)
        elif isinstance(obj.dtype, pd.StringDtype):
            return obj.dtype.storage == "python"
        return is_object_dtype(obj)

    has_objects = _is_object_dtype(obj) or (is_ser and _is_object_dtype(obj.index))

    if len(obj) == 0:
        expected = 0
        assert res_deep == res == expected
    elif has_objects:
        # only deep will pick them up
        assert res_deep > res
    else:
        assert res == res_deep

    # sys.getsizeof will call the .memory_usage with
    # deep=True, and add on some GC overhead
    diff = res_deep - sys.getsizeof(obj)
    assert abs(diff) < 100


def test_memory_usage(idx):
    result = idx.memory_usage()
    if len(idx):
        idx.get_loc(idx[0])
        result2 = idx.memory_usage()
        result3 = idx.memory_usage(deep=True)

        # RangeIndex, IntervalIndex
        # don't have engines
        if not isinstance(idx, (RangeIndex, IntervalIndex)):
            assert result2 > result

        if idx.inferred_type == "object":
            assert result3 > result2

    else:
        # we report 0 for no-length
        assert result == 0


def test_memory_usage(dtype):
    # GH 33963

    if dtype.storage == "pyarrow":
        pytest.skip(f"not applicable for {dtype.storage}")

    series = pd.Series(["a", "b", "c"], dtype=dtype)

    assert 0 < series.nbytes <= series.memory_usage() < series.memory_usage(deep=True)

