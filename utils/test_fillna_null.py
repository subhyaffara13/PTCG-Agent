
def test_fillna_null(null_obj, index_or_series_obj):
    # GH 11343
    obj = index_or_series_obj
    klass = type(obj)

    if not allow_na_ops(obj):
        pytest.skip(f"{klass} doesn't allow for NA operations")
    elif len(obj) < 1:
        pytest.skip("Test doesn't make sense on empty data")
    elif isinstance(obj, MultiIndex):
        pytest.skip(f"MultiIndex can't hold '{null_obj}'")

    obj = obj.copy(deep=True)
    values = obj._values
    fill_value = values[0]
    expected = values.copy()
    values[0:2] = null_obj
    expected[0:2] = fill_value

    expected = klass(expected)
    obj = klass(values)

    result = obj.fillna(fill_value)
    tm.assert_equal(result, expected)

    # check shallow_copied
    assert obj is not result

