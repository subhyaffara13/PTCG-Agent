
def test_repr_array():
    result = repr(pd.array([1.0, None, 3.0]))
    expected = "<FloatingArray>\n[1.0, <NA>, 3.0]\nLength: 3, dtype: Float64"
    assert result == expected


def test_repr_array():
    result = repr(pd.array([1, None, 3]))
    expected = "<IntegerArray>\n[1, <NA>, 3]\nLength: 3, dtype: Int64"
    assert result == expected

