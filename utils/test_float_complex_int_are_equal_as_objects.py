
def test_float_complex_int_are_equal_as_objects():
    values = ["a", 5, 5.0, 5.0 + 0j]
    comps = list(range(129))
    result = isin(np.array(values, dtype=object), np.asarray(comps))
    expected = np.array([False, True, True, True], dtype=np.bool_)
    tm.assert_numpy_array_equal(result, expected)

