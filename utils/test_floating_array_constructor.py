
def test_floating_array_constructor():
    values = np.array([1, 2, 3, 4], dtype="float64")
    mask = np.array([False, False, False, True], dtype="bool")

    result = FloatingArray(values, mask)
    expected = pd.array([1, 2, 3, pd.NA], dtype="Float64")
    tm.assert_extension_array_equal(result, expected)
    tm.assert_numpy_array_equal(result._data, values)
    tm.assert_numpy_array_equal(result._mask, mask)

    msg = r".* should be .* numpy array. Use the 'pd.array' function instead"
    with pytest.raises(TypeError, match=msg):
        FloatingArray(values.tolist(), mask)

    with pytest.raises(TypeError, match=msg):
        FloatingArray(values, mask.tolist())

    with pytest.raises(TypeError, match=msg):
        FloatingArray(values.astype(int), mask)

    msg = r"__init__\(\) missing 1 required positional argument: 'mask'"
    with pytest.raises(TypeError, match=msg):
        FloatingArray(values)

