
def test_mixed_str_null(nulls_fixture):
    values = np.array(["b", nulls_fixture, "a", "b"], dtype=object)
    result = safe_sort(values)
    expected = np.array(["a", "b", "b", nulls_fixture], dtype=object)
    tm.assert_numpy_array_equal(result, expected)

