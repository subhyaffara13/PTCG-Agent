
def test_repr_array_long():
    data = pd.array([1.0, 2.0, None] * 1000)
    expected = """<FloatingArray>
[ 1.0,  2.0, <NA>,  1.0,  2.0, <NA>,  1.0,  2.0, <NA>,  1.0,
 ...
 <NA>,  1.0,  2.0, <NA>,  1.0,  2.0, <NA>,  1.0,  2.0, <NA>]
Length: 3000, dtype: Float64"""
    result = repr(data)
    assert result == expected


def test_repr_array_long():
    data = pd.array([1, 2, None] * 1000)
    expected = (
        "<IntegerArray>\n"
        "[   1,    2, <NA>,    1,    2, <NA>,    1,    2, <NA>,    1,\n"
        " ...\n"
        " <NA>,    1,    2, <NA>,    1,    2, <NA>,    1,    2, <NA>]\n"
        "Length: 3000, dtype: Int64"
    )
    result = repr(data)
    assert result == expected

