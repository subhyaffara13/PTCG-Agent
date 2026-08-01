
def test_is_bool_dtype():
    assert not com.is_bool_dtype(int)
    assert not com.is_bool_dtype(str)
    assert not com.is_bool_dtype(pd.Series([1, 2]))
    assert not com.is_bool_dtype(pd.Series(["a", "b"], dtype="category"))
    assert not com.is_bool_dtype(np.array(["a", "b"]))
    assert not com.is_bool_dtype(pd.Index(["a", "b"]))
    assert not com.is_bool_dtype("Int64")

    assert com.is_bool_dtype(bool)
    assert com.is_bool_dtype(np.bool_)
    assert com.is_bool_dtype(pd.Series([True, False], dtype="category"))
    assert com.is_bool_dtype(np.array([True, False]))
    assert com.is_bool_dtype(pd.Index([True, False]))

    assert com.is_bool_dtype(pd.BooleanDtype())
    assert com.is_bool_dtype(pd.array([True, False, None], dtype="boolean"))
    assert com.is_bool_dtype("boolean")


def test_is_bool_dtype(dtype, expected):
    result = is_bool_dtype(dtype)
    assert result is expected


def test_is_bool_dtype():
    # GH 22667
    data = ArrowExtensionArray(pa.array([True, False, True]))
    assert is_bool_dtype(data)
    assert pd.core.common.is_bool_indexer(data)
    s = pd.Series(range(len(data)))
    result = s[data]
    expected = s[np.asarray(data)]
    tm.assert_series_equal(result, expected)

