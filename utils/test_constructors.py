
def test_constructors():
    defaults = m.default_constructors()
    for a in defaults.values():
        assert a.size == 0
    assert defaults["array"].dtype == np.array([]).dtype
    assert defaults["array_t<int32>"].dtype == np.int32
    assert defaults["array_t<double>"].dtype == np.float64

    results = m.converting_constructors([1, 2, 3])
    for a in results.values():
        np.testing.assert_array_equal(a, [1, 2, 3])
    assert results["array"].dtype == np.int_
    assert results["array_t<int32>"].dtype == np.int32
    assert results["array_t<double>"].dtype == np.float64


def test_constructors():
    """C++ default and converting constructors are equivalent to type calls in Python"""
    types = [bytes, bytearray, str, bool, int, float, tuple, list, dict, set]
    expected = {t.__name__: t() for t in types}
    assert m.default_constructors() == expected

    data = {
        bytes: b"41",  # Currently no supported or working conversions.
        bytearray: bytearray(b"41"),
        str: 42,
        bool: "Not empty",
        int: "42",
        float: "+1e3",
        tuple: range(3),
        list: range(3),
        dict: [("two", 2), ("one", 1), ("three", 3)],
        set: [4, 4, 5, 6, 6, 6],
        frozenset: [4, 4, 5, 6, 6, 6],
        memoryview: b"abc",
    }
    inputs = {k.__name__: v for k, v in data.items()}
    expected = {k.__name__: k(v) for k, v in data.items()}

    assert m.converting_constructors(inputs) == expected
    assert m.cast_functions(inputs) == expected

    # Converting constructors and cast functions should just reference rather
    # than copy when no conversion is needed:
    noconv1 = m.converting_constructors(expected)
    for k in noconv1:
        assert noconv1[k] is expected[k]

    noconv2 = m.cast_functions(expected)
    for k in noconv2:
        assert noconv2[k] is expected[k]

